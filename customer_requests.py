import json
import os
from datetime import datetime
from database import db
from psycopg2.extras import RealDictCursor


class CustomerRequests:
    """Manages customer part requests - supports both PostgreSQL and JSON"""

    def __init__(self, db_path='customer_requests.json'):
        self.db_path = db_path
        self.use_postgres = db.enabled

        if not self.use_postgres:
            # Use JSON file for local development
            self.requests = self.load()

    def load(self):
        """Load requests from JSON file (fallback for local)"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save(self):
        """Save requests to JSON file (fallback for local)"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.requests, f, indent=2, ensure_ascii=False)

    def add_request(self, request_data):
        """Add a new customer request"""
        if self.use_postgres:
            return self._add_request_postgres(request_data)
        else:
            return self._add_request_json(request_data)

    def _add_request_postgres(self, request_data):
        """Add request to PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Convert part_images list to JSON string
        part_images_json = json.dumps(request_data.get('part_images', []))

        cursor.execute("""
            INSERT INTO customer_requests (
                date, time, customer_name, customer_phone, customer_email,
                vehicle_year, vehicle_make, vehicle_model, vehicle_color,
                color_doesnt_matter, compatible_models, pyp_location, mileage,
                part_needed, part_size, junkyard_parts, part_images,
                additional_notes, secure_method, warranty, wants_warranty,
                language, status, quote_amount, quote_message, deposit_amount,
                deposit_required, deposit_paid, photos_sent, response_message,
                created_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING *
        """, (
            datetime.now().strftime('%Y-%m-%d'),
            datetime.now().strftime('%I:%M %p'),
            request_data.get('customer_name', ''),
            request_data.get('customer_phone', ''),
            request_data.get('customer_email', ''),
            request_data.get('vehicle_year', ''),
            request_data.get('vehicle_make', ''),
            request_data.get('vehicle_model', ''),
            request_data.get('vehicle_color', ''),
            request_data.get('color_doesnt_matter', False),
            request_data.get('compatible_models', ''),
            request_data.get('pyp_location', ''),
            request_data.get('mileage', 0),
            request_data.get('part_needed', ''),
            request_data.get('part_size', '40'),
            request_data.get('junkyard_parts', ''),
            part_images_json,
            request_data.get('additional_notes', ''),
            request_data.get('secure_method', ''),
            request_data.get('warranty', False),
            request_data.get('wants_warranty', False),
            request_data.get('language', 'en'),
            'new',
            0,
            '',
            request_data.get('deposit_amount', '0'),
            True,
            False,
            False,
            '',
            datetime.now()
        ))

        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        # Convert result to dict and parse JSON fields
        request = dict(result)
        request['part_images'] = json.loads(request.get('part_images', '[]'))
        return request

    def _add_request_json(self, request_data):
        """Add request to JSON file"""
        # Get the maximum ID to avoid collisions when requests are deleted
        max_id = max([r.get('id', 0) for r in self.requests], default=0)
        request = {
            'id': max_id + 1,
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
            'deposit_amount': request_data.get('deposit_amount', '0'),
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
        if self.use_postgres:
            return self._update_request_postgres(request_id, updates)
        else:
            return self._update_request_json(request_id, updates)

    def _update_request_postgres(self, request_id, updates):
        """Update request in PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        for key, value in updates.items():
            if key != 'id':
                set_clauses.append(f"{key} = %s")
                values.append(value)

        set_clauses.append("updated_at = %s")
        values.append(datetime.now())
        values.append(request_id)

        query = f"""
            UPDATE customer_requests
            SET {', '.join(set_clauses)}
            WHERE id = %s
            RETURNING *
        """

        cursor.execute(query, values)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        if result:
            request = dict(result)
            if 'part_images' in request:
                request['part_images'] = json.loads(request.get('part_images', '[]'))
            return request
        return None

    def _update_request_json(self, request_id, updates):
        """Update request in JSON file"""
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
        if self.use_postgres:
            return self._delete_request_postgres(request_id)
        else:
            return self._delete_request_json(request_id)

    def _delete_request_postgres(self, request_id):
        """Delete request from PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM customer_requests WHERE id = %s", (request_id,))
        deleted = cursor.rowcount > 0

        conn.commit()
        cursor.close()
        conn.close()
        return deleted

    def _delete_request_json(self, request_id):
        """Delete request from JSON file"""
        initial_length = len(self.requests)
        self.requests = [r for r in self.requests if r['id'] != request_id]
        if len(self.requests) < initial_length:
            self.save()
            return True
        return False

    def get_all_requests(self):
        """Get all requests sorted by newest first"""
        if self.use_postgres:
            return self._get_all_requests_postgres()
        else:
            return sorted(self.requests, key=lambda x: x.get('created_at', ''), reverse=True)

    def _get_all_requests_postgres(self):
        """Get all requests from PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM customer_requests ORDER BY created_at DESC")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert to list of dicts and parse JSON fields
        requests = []
        for row in results:
            request = dict(row)
            request['part_images'] = json.loads(request.get('part_images', '[]'))
            requests.append(request)

        return requests

    def get_by_status(self, status):
        """Get requests by status"""
        if self.use_postgres:
            return self._get_by_status_postgres(status)
        else:
            return [r for r in self.requests if r.get('status') == status]

    def _get_by_status_postgres(self, status):
        """Get requests by status from PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM customer_requests WHERE status = %s ORDER BY created_at DESC", (status,))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        requests = []
        for row in results:
            request = dict(row)
            request['part_images'] = json.loads(request.get('part_images', '[]'))
            requests.append(request)

        return requests

    def get_stats(self):
        """Get statistics"""
        if self.use_postgres:
            return self._get_stats_postgres()
        else:
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

    def _get_stats_postgres(self):
        """Get statistics from PostgreSQL"""
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM customer_requests")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customer_requests WHERE status = 'new'")
        new = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customer_requests WHERE status = 'quoted'")
        quoted = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM customer_requests WHERE status = 'completed'")
        completed = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return {
            'total': total,
            'new': new,
            'quoted': quoted,
            'completed': completed
        }
