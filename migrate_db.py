import os
import sqlite3
import re
from urllib.parse import urlparse


def _resolve_db_path(app):
    if app is not None:
        uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///autosolo.db')
        instance_path = app.instance_path
    else:
        uri = 'sqlite:///autosolo.db'
        instance_path = os.getcwd()

    if uri.startswith('sqlite:///'):
        parsed = urlparse(uri)
        raw_path = parsed.path or uri.replace('sqlite:///', '', 1)

        if os.name == 'nt':
            # Strip a single leading slash for Windows drive-letter paths (/C:/foo -> C:/foo)
            if raw_path.startswith('/') and len(raw_path) > 2 and raw_path[2] == ':':
                raw_path = raw_path[1:]
        
        if os.path.isabs(raw_path) or (os.name == 'nt' and len(raw_path) > 1 and raw_path[1] == ':'):
            resolved = raw_path
        else:
            base_dir = instance_path if app is not None else os.getcwd()
            resolved = os.path.join(base_dir, raw_path.lstrip('/'))

        resolved = os.path.abspath(resolved)
        os.makedirs(os.path.dirname(resolved), exist_ok=True)
        return resolved

    raise ValueError('ensure_schema only supports sqlite:/// URIs')


def ensure_schema(app=None, db=None, verbose=True):
    """Create or evolve the SQLite schema for the car table."""
    db_path = _resolve_db_path(app)
    creating = not os.path.exists(db_path)

    if creating:
        if verbose:
            print(f"Database {db_path} does not exist. Creating new database...")

        if app is None or db is None:
            from app import app as flask_app, db as flask_db  # Lazy import to avoid circular deps
        else:
            flask_app, flask_db = app, db

        with flask_app.app_context():
            flask_db.create_all()

        if verbose:
            print("✓ New database created with updated schema!")

    if verbose:
        print(f"Migrating database {db_path}...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(car)")
    table_info = cursor.fetchall()
    column_names = {col[1] for col in table_info}

    def add_column(column_name, sql, message):
        if column_name not in column_names:
            if verbose:
                print(message)
            cursor.execute(sql)
            column_names.add(column_name)

    add_column('engine_liters', 'ALTER TABLE car ADD COLUMN engine_liters TEXT', "Adding engine_liters column...")
    add_column('engine_cylinders', 'ALTER TABLE car ADD COLUMN engine_cylinders TEXT', "Adding engine_cylinders column...")
    add_column('fuel_type', 'ALTER TABLE car ADD COLUMN fuel_type TEXT', "Adding fuel_type column...")
    add_column('contact_number', 'ALTER TABLE car ADD COLUMN contact_number TEXT', "Adding contact_number column...")
    add_column('mileage_unit', "ALTER TABLE car ADD COLUMN mileage_unit TEXT DEFAULT 'km'", "Adding mileage_unit column with default 'km'...")
    add_column('views', 'ALTER TABLE car ADD COLUMN views INTEGER DEFAULT 0', "Adding views column with default 0...")

    if 'engine' in column_names and 'engine_liters' in column_names:
        if verbose:
            print("Migrating engine data...")
        cursor.execute('SELECT id, engine FROM car WHERE engine IS NOT NULL')
        cars = cursor.fetchall()

        for car_id, engine_text in cars:
            if not engine_text:
                continue

            liters_match = re.search(r'(\d+\.?\d*)[Ll]', engine_text)
            if liters_match:
                liters = liters_match.group(0)
                cursor.execute('UPDATE car SET engine_liters = ? WHERE id = ?', (liters, car_id))

            cyl_patterns = [r'[Vv](\d+)', r'(\d+)-?cyl', r'[Ii]nline-?(\d+)']
            for pattern in cyl_patterns:
                cyl_match = re.search(pattern, engine_text)
                if cyl_match:
                    cylinders = f"V{cyl_match.group(1)}" if 'V' in pattern else f"{cyl_match.group(1)}-cylinder"
                    cursor.execute('UPDATE car SET engine_cylinders = ? WHERE id = ?', (cylinders, car_id))
                    break

    conn.commit()

    if verbose:
        cursor.execute("PRAGMA table_info(car)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print("✓ Database migration completed! Columns:", final_columns)

    conn.close()


if __name__ == '__main__':
    ensure_schema()
    print("\nYou can now restart your Flask server and test the new features!")
