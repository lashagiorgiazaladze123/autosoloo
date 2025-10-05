import sqlite3
import os

# Connect to database
db_path = 'autoslo.db'

if not os.path.exists(db_path):
    print(f"Database {db_path} does not exist. Creating new database...")
    from app import app, db
    app.app_context().push()
    db.create_all()
    print("✓ New database created with updated schema!")
else:
    print(f"Migrating database {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(car)")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"Current columns: {column_names}")
    
    # Add new columns if they don't exist
    if 'engine_liters' not in column_names:
        print("Adding engine_liters column...")
        cursor.execute('ALTER TABLE car ADD COLUMN engine_liters TEXT')
    
    if 'engine_cylinders' not in column_names:
        print("Adding engine_cylinders column...")
        cursor.execute('ALTER TABLE car ADD COLUMN engine_cylinders TEXT')
    
    if 'fuel_type' not in column_names:
        print("Adding fuel_type column...")
        cursor.execute('ALTER TABLE car ADD COLUMN fuel_type TEXT')
    
    # Migrate data from old 'engine' column if it exists
    if 'engine' in column_names and 'engine_liters' in column_names:
        print("Migrating engine data...")
        cursor.execute('SELECT id, engine FROM car WHERE engine IS NOT NULL')
        cars = cursor.fetchall()
        
        for car_id, engine_text in cars:
            if engine_text:
                # Try to extract engine liters (e.g., "2.5L")
                import re
                liters_match = re.search(r'(\d+\.?\d*)[Ll]', engine_text)
                if liters_match:
                    liters = liters_match.group(0)
                    cursor.execute('UPDATE car SET engine_liters = ? WHERE id = ?', (liters, car_id))
                
                # Try to extract cylinder info (e.g., "V6", "V8", "4-cylinder")
                cyl_patterns = [r'[Vv](\d+)', r'(\d+)-?cyl', r'[Ii]nline-?(\d+)']
                for pattern in cyl_patterns:
                    cyl_match = re.search(pattern, engine_text)
                    if cyl_match:
                        cylinders = f"V{cyl_match.group(1)}" if 'V' in pattern else f"{cyl_match.group(1)}-cylinder"
                        cursor.execute('UPDATE car SET engine_cylinders = ? WHERE id = ?', (cylinders, car_id))
                        break
    
    conn.commit()
    conn.close()
    print("✓ Database migration completed!")

print("\nYou can now restart your Flask server and test the new features!")
