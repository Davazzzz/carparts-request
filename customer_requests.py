import json
from datetime import datetime


class CustomerRequests:
    """Manages customer part requests"""

    def __init__(self, db_path='customer_requests.json'):
        self.db_path = db_path
        self.requests = self.load()

    def load(self):
        """Load requests from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        """Save requests to JSON file"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.requests, f, indent=2, ensure_ascii=False)

    def add_request(self, request_data):
        """Add a new customer request"""
        request = {
            'id': len(self.requests) + 1,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%I:%M %p'),
            'customer_name': request_data.get('customer_name', ''),
            'customer_phone': request_data.get('customer_phone', ''),
            'customer_email': request_data.get('customer_email', ''),
            'vehicle_year': request_data.get('vehicle_year', ''),
            'vehicle_make': request_data.get('vehicle_make', ''),
            'vehicle_model': request_data.get('vehicle_model', ''),
            'vehicle_color': request_data.get('vehicle_color', ''),
            'color_doesnt_matter': request_data.get('color_doesnt_matter', False),
            'compatible_models': request_data.get('compatible_models', ''),
            'pyp_location': request_data.get('pyp_location', ''),
            'mileage': request_data.get('mileage', 0),
            'part_needed': request_data.get('part_needed', ''),
            'part_size': request_data.get('part_size', '40'),
            'junkyard_parts': request_data.get('junkyard_parts', ''),
            'part_images': request_data.get('part_images', []),
            'additional_notes': request_data.get('additional_notes', ''),
            'secure_method': request_data.get('secure_method', ''),
            'warranty': request_data.get('warranty', False),
            'wants_warranty': request_data.get('wants_warranty', False),
            'language': request_data.get('language', 'en'),
            'status': 'new',
            'quote_amount': 0,
            'quote_message': '',
            'deposit_amount': 0,
            'deposit_required': True,
            'deposit_paid': False,
            'photos_sent': False,
            'response_message': '',
            'created_at': datetime.now().isoformat()
        }

        self.requests.append(request)
        self.save()
        return request

    def update_request(self, request_id, updates):
        """Update an existing request"""
        for req in self.requests:
            if req['id'] == request_id:
                for key, value in updates.items():
                    if key != 'id':
                        req[key] = value
                req['updated_at'] = datetime.now().isoformat()
                self.save()
                return req
        return None

    def delete_request(self, request_id):
        """Delete a request"""
        initial_length = len(self.requests)
        self.requests = [r for r in self.requests if r['id'] != request_id]
        if len(self.requests) < initial_length:
            self.save()
            return True
        return False

    def get_all_requests(self):
        """Get all requests sorted by newest first"""
        return sorted(self.requests, key=lambda x: x.get('created_at', ''), reverse=True)

    def get_by_status(self, status):
        """Get requests by status"""
        return [r for r in self.requests if r.get('status') == status]

    def get_stats(self):
        """Get statistics"""
        total = len(self.requests)
        new = len([r for r in self.requests if r.get('status') == 'new'])
        quoted = len([r for r in self.requests if r.get('status') == 'quoted'])
        completed = len([r for r in self.requests if r.get('status') == 'completed'])

        return {
            'total': total,
            'new': new,
            'quoted': quoted,
            'completed': completed
        }
