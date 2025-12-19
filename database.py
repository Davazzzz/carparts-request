import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse

class Database:
    """Handles PostgreSQL database connections"""

    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        if not self.database_url:
            # Fallback to JSON if no database URL (local development)
            self.enabled = False
        else:
            self.enabled = True
            self.init_db()

    def get_connection(self):
        """Get a database connection"""
        if not self.enabled:
            return None
        return psycopg2.connect(self.database_url)

    def init_db(self):
        """Initialize database schema"""
        if not self.enabled:
            return

        conn = self.get_connection()
        cursor = conn.cursor()

        # Create customer_requests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_requests (
                id SERIAL PRIMARY KEY,
                date VARCHAR(20),
                time VARCHAR(20),
                customer_name VARCHAR(255),
                customer_phone VARCHAR(50),
                customer_email VARCHAR(255),
                vehicle_year VARCHAR(10),
                vehicle_make VARCHAR(100),
                vehicle_model VARCHAR(100),
                vehicle_color VARCHAR(50),
                color_doesnt_matter BOOLEAN DEFAULT FALSE,
                compatible_models TEXT,
                pyp_location VARCHAR(255),
                mileage INTEGER DEFAULT 0,
                part_needed TEXT,
                part_size VARCHAR(10),
                junkyard_parts TEXT,
                part_images TEXT,
                additional_notes TEXT,
                secure_method VARCHAR(50),
                warranty BOOLEAN DEFAULT FALSE,
                wants_warranty BOOLEAN DEFAULT FALSE,
                language VARCHAR(10) DEFAULT 'en',
                status VARCHAR(50) DEFAULT 'new',
                quote_amount DECIMAL(10,2) DEFAULT 0,
                quote_message TEXT,
                deposit_amount VARCHAR(10) DEFAULT '0',
                deposit_required BOOLEAN DEFAULT TRUE,
                deposit_paid BOOLEAN DEFAULT FALSE,
                photos_sent BOOLEAN DEFAULT FALSE,
                response_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()

# Global database instance
db = Database()
