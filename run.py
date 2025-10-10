from app import app, db
from migrate_db import ensure_schema
import logging

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    ensure_schema(app, db)
    app.run(debug=True, host='0.0.0.0')