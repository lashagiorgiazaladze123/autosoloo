from app import app, db
from migrate_db import ensure_schema

if __name__ == '__main__':
    ensure_schema(app, db)
    app.run(debug=True, host='0.0.0.0', port=5000)