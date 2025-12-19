from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from customer_requests import CustomerRequests
from junkyard_prices import JunkyardPrices
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-8x9z2k4m5n6p7q')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize customer requests handler
requests_db = CustomerRequests('customer_requests.json')

# Initialize junkyard prices
junkyard_prices = JunkyardPrices('Junkyard Pricing.csv')


# ==================== CUSTOMER-FACING ROUTES ====================

@app.route('/')
def index():
    """Customer landing page with language selection"""
    return render_template('index.html')


@app.route('/request')
def request_form():
    """Customer request form"""
    language = request.args.get('lang', 'en')
    return render_template('request_form.html', language=language)


@app.route('/submit_request', methods=['POST'])
def submit_request():
    """Handle customer request submission"""
    try:
        # Handle both JSON and form data (for file uploads)
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Handle form data with files
            data = {
                'customer_name': request.form.get('customer_name'),
                'customer_phone': request.form.get('customer_phone'),
                'vehicle_year': request.form.get('vehicle_year'),
                'vehicle_make': request.form.get('vehicle_make'),
                'vehicle_model': request.form.get('vehicle_model'),
                'vehicle_color': request.form.get('vehicle_color'),
                'color_doesnt_matter': request.form.get('color_doesnt_matter') == 'true',
                'part_needed': request.form.get('part_needed'),
                'additional_notes': request.form.get('additional_notes'),
                'secure_method': request.form.get('secure_method'),
                'warranty': request.form.get('warranty') == 'true',
                'deposit_amount': request.form.get('deposit_amount', '0'),
                'language': request.form.get('language'),
                'junkyard_parts': request.form.get('junkyard_parts'),  # JSON string
                'part_images': []
            }

            # Handle multiple file uploads
            if 'part_images[]' in request.files:
                files = request.files.getlist('part_images[]')
                for file in files:
                    if file and file.filename:
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        data['part_images'].append(filename)
        else:
            # Handle JSON data
            data = request.json

        new_request = requests_db.add_request(data)

        return jsonify({
            'success': True,
            'message': 'Request submitted successfully!',
            'request_id': new_request['id']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/thank_you')
def thank_you():
    """Thank you page after submission"""
    import json
    language = request.args.get('lang', 'en')
    request_id = request.args.get('request_id')

    # Get the submitted request data if request_id is provided
    submitted_data = None
    if request_id:
        all_requests = requests_db.get_all_requests()
        for req in all_requests:
            if str(req.get('id')) == str(request_id):
                submitted_data = req

                # Parse junkyard_parts JSON if it exists
                if submitted_data.get('junkyard_parts'):
                    try:
                        junkyard_parts_str = submitted_data.get('junkyard_parts')
                        if isinstance(junkyard_parts_str, str) and junkyard_parts_str not in ['', '[]']:
                            submitted_data['junkyard_parts_list'] = json.loads(junkyard_parts_str)
                        else:
                            submitted_data['junkyard_parts_list'] = []
                    except:
                        submitted_data['junkyard_parts_list'] = []
                else:
                    submitted_data['junkyard_parts_list'] = []
                break

    return render_template('thank_you.html', language=language, data=submitted_data)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== JUNKYARD PARTS ROUTES ====================

@app.route('/junkyard_parts')
def get_junkyard_parts():
    """Get all junkyard parts with prices"""
    all_parts = junkyard_prices.get_all_parts()
    parts_with_prices = []

    for part in all_parts:
        price = junkyard_prices.get_price(part)
        if price:
            parts_with_prices.append({
                'name': part,
                'price': price
            })

    return jsonify({
        'success': True,
        'parts': parts_with_prices
    })


@app.route('/search_junkyard_parts')
def search_junkyard_parts():
    """Search junkyard parts by keyword"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            'success': True,
            'parts': []
        })

    matches = junkyard_prices.search_part(query)
    parts_list = [
        {'name': name, 'price': price}
        for name, price in matches.items()
    ]

    return jsonify({
        'success': True,
        'parts': parts_list
    })


# ==================== ADMIN PANEL ROUTES ====================

@app.route('/admin')
def admin_panel():
    """Admin dashboard to manage requests"""
    return render_template('admin.html')


@app.route('/admin/requests', methods=['GET'])
def get_requests():
    """Get all customer requests"""
    all_requests = requests_db.get_all_requests()
    stats = requests_db.get_stats()

    return jsonify({
        'success': True,
        'requests': all_requests,
        'stats': stats
    })


@app.route('/admin/request/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    """Update a request (send quote, mark as complete, etc.)"""
    try:
        data = request.json
        updated = requests_db.update_request(request_id, data)

        if updated:
            return jsonify({
                'success': True,
                'request': updated
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Request not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/request/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    """Delete a request"""
    try:
        success = requests_db.delete_request(request_id)

        if success:
            return jsonify({
                'success': True,
                'message': 'Request deleted'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Request not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/admin/delete_all', methods=['DELETE'])
def delete_all_requests():
    """Delete all requests"""
    try:
        all_requests = requests_db.get_all_requests()
        deleted_count = len(all_requests)

        # Delete each request
        for req in all_requests:
            requests_db.delete_request(req['id'])

        return jsonify({
            'success': True,
            'message': 'All requests deleted',
            'deleted_count': deleted_count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    import os

    print("\n" + "="*60)
    print("Parts Request Website")
    print("="*60)

    # Use PORT from environment (for Railway/production) or 5001 for local
    port = int(os.environ.get('PORT', 5001))

    print(f"\nCustomer Page: http://localhost:{port}")
    print(f"Admin Panel: http://localhost:{port}/admin")
    print("="*60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=port)
