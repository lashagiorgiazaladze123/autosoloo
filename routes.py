from app import app, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import User, Car
from werkzeug.utils import secure_filename
import os
import json

FEATURES_OPTIONS = [
    'Air conditioner', 'Climate control', 'Wheels', 'Electric windows', 'Rear view camera',
    'Onboard computer', 'Seat heating', 'Hydraulics', 'Turbo', 'Navigation',
    'Parking control', 'Adapted for disabled', 'Start-stop system', 'Sunroof',
    'Cruise control', 'Multi steering wheel', 'Alarm'
]

@app.route('/')
def index():
    cars = Car.query.all()
    return render_template('index.html', cars=cars)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = {}
    if request.method == 'POST':
        # Collect all filters from form
        query['make'] = request.form.get('make')
        query['model'] = request.form.get('model')
        query['min_year'] = request.form.get('min_year')
        query['max_year'] = request.form.get('max_year')
        query['min_price'] = request.form.get('min_price')
        query['max_price'] = request.form.get('max_price')
        query['engine'] = request.form.get('engine')
        query['min_mileage'] = request.form.get('min_mileage')
        query['max_mileage'] = request.form.get('max_mileage')
        query['category'] = request.form.get('category')
        query['gearbox'] = request.form.get('gearbox')
        query['steering'] = request.form.getlist('steering')  # multi
        query['drive'] = request.form.getlist('drive')  # multi
        query['doors'] = request.form.getlist('doors')  # multi
        query['tech_inspection'] = request.form.get('tech_inspection')
        query['catalyst'] = request.form.get('catalyst')
        query['features'] = request.form.getlist('features')
        query['colors'] = request.form.getlist('colors')
        query['interior_material'] = request.form.get('interior_material')
        query['interior_colors'] = request.form.getlist('interior_colors')

    # Build query
    cars_query = Car.query
    if query.get('make'):
        cars_query = cars_query.filter(Car.make.ilike(f"%{query['make']}%"))
    if query.get('model'):
        cars_query = cars_query.filter(Car.model.ilike(f"%{query['model']}%"))
    if query.get('min_year'):
        cars_query = cars_query.filter(Car.year >= int(query['min_year']))
    if query.get('max_year'):
        cars_query = cars_query.filter(Car.year <= int(query['max_year']))
    if query.get('min_price'):
        cars_query = cars_query.filter(Car.price >= float(query['min_price']))
    if query.get('max_price'):
        cars_query = cars_query.filter(Car.price <= float(query['max_price']))
    if query.get('engine'):
        cars_query = cars_query.filter(Car.engine.ilike(f"%{query['engine']}%"))
    if query.get('min_mileage'):
        cars_query = cars_query.filter(Car.mileage >= int(query['min_mileage']))
    if query.get('max_mileage'):
        cars_query = cars_query.filter(Car.mileage <= int(query['max_mileage']))
    if query.get('category'):
        cars_query = cars_query.filter(Car.category == query['category'])
    if query.get('gearbox'):
        cars_query = cars_query.filter(Car.gearbox == query['gearbox'])
    if query.get('steering'):
        cars_query = cars_query.filter(Car.steering.in_(query['steering']))
    if query.get('drive'):
        cars_query = cars_query.filter(Car.drive.in_(query['drive']))
    if query.get('doors'):
        cars_query = cars_query.filter(Car.doors.in_(query['doors']))
    if query.get('tech_inspection'):
        tech_bool = query['tech_inspection'] == 'Yes'
        cars_query = cars_query.filter(Car.tech_inspection == tech_bool)
    if query.get('catalyst'):
        cat_bool = query['catalyst'] == 'Yes'
        cars_query = cars_query.filter(Car.catalyst == cat_bool)
    if query.get('features'):
        for feature in query['features']:
            cars_query = cars_query.filter(Car.features.contains(feature))
    if query.get('colors'):
        cars_query = cars_query.filter(Car.color.in_(query['colors']))
    if query.get('interior_material'):
        cars_query = cars_query.filter(Car.interior_material == query['interior_material'])
    if query.get('interior_colors'):
        cars_query = cars_query.filter(Car.interior_color.in_(query['interior_colors']))

    cars = cars_query.all()
    return render_template('search.html', cars=cars, features_options=FEATURES_OPTIONS)
@app.route('/car/<int:car_id>')
def car_detail(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('car_detail.html', car=car)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # Get required fields
        make = request.form.get('make', '')
        model = request.form.get('model', '')
        year = request.form.get('year', '0')
        price = request.form.get('price', '0')
        
        # Get optional fields with defaults
        engine = request.form.get('engine', '')
        mileage = request.form.get('mileage', '0')
        category = request.form.get('category', '')
        gearbox = request.form.get('gearbox', '')
        steering = request.form.get('steering', '')
        drive = request.form.get('drive', '')
        doors = request.form.get('doors', '')
        tech_inspection_value = request.form.get('tech_inspection', '')
        catalyst_value = request.form.get('catalyst', '')
        color = request.form.get('color', '')
        interior_material = request.form.get('interior_material', '')
        interior_color = request.form.get('interior_color', '')
        description = request.form.get('description', '')
        
        # Convert to boolean
        tech_inspection = tech_inspection_value == 'Yes' if tech_inspection_value else False
        catalyst = catalyst_value == 'Yes' if catalyst_value else False
        
        # Convert numeric fields safely
        try:
            year_int = int(year) if year else 0
        except ValueError:
            year_int = 0
            
        try:
            price_float = float(price) if price else 0.0
        except ValueError:
            price_float = 0.0
            
        try:
            mileage_int = int(mileage) if mileage else 0
        except ValueError:
            mileage_int = 0
        
        # Create car object
        car = Car(
            make=make,
            model=model,
            year=year_int,
            price=price_float,
            engine=engine,
            mileage=mileage_int,
            category=category,
            gearbox=gearbox,
            steering=steering,
            drive=drive,
            doors=doors,
            tech_inspection=tech_inspection,
            catalyst=catalyst,
            color=color,
            interior_material=interior_material,
            interior_color=interior_color,
            description=description,
            user_id=current_user.id
        )
        
        # Handle features
        features = request.form.getlist('features')
        if features:
            car.set_features(features)

        # Handle image uploads
        images = []
        for file in request.files.getlist('images'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                # Store relative path for templates
                images.append(f'uploads/{filename}')
        
        if images:
            car.set_images(images)

        db.session.add(car)
        db.session.commit()
        flash('Car uploaded successfully!')
        return redirect(url_for('profile'))

    return render_template('upload.html', features_options=FEATURES_OPTIONS)

@app.route('/profile')
@login_required
def profile():
    cars = current_user.cars.all()
    return render_template('profile.html', cars=cars)

@app.route('/delete_car/<int:car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('profile'))
    db.session.delete(car)
    db.session.commit()
    flash('Car deleted')
    return redirect(url_for('profile'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('Registered successfully')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/favorites')
@login_required
def favorites():
    favorite_cars = current_user.favorite_cars.all()
    return render_template('favorites.html', cars=favorite_cars)

@app.route('/toggle_favorite/<int:car_id>', methods=['POST'])
@login_required
def toggle_favorite(car_id):
    car = Car.query.get_or_404(car_id)
    
    if current_user.has_favorited(car):
        current_user.remove_favorite(car)
        db.session.commit()
        return {'status': 'removed', 'favorited': False}, 200
    else:
        current_user.add_favorite(car)
        db.session.commit()
        return {'status': 'added', 'favorited': True}, 200