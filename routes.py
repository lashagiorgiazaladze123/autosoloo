from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import User, Car
from werkzeug.utils import secure_filename
import os
import json
from car_data import (
    CAR_MAKES_MODELS, ENGINE_LITERS, ENGINE_CYLINDERS, YEARS, 
    CATEGORIES, GEARBOX_OPTIONS, STEERING_OPTIONS, DRIVE_OPTIONS,
    DOORS_OPTIONS, COLORS, INTERIOR_MATERIALS, INTERIOR_COLORS, FUEL_TYPES
)

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

@app.route('/api/get-models/<make>')
def get_models(make):
    """API endpoint to get models for a specific make"""
    models = CAR_MAKES_MODELS.get(make, [])
    return jsonify(models)

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
        engine_liters = request.form.get('engine_liters', '')
        engine_cylinders = request.form.get('engine_cylinders', '')
        fuel_type = request.form.get('fuel_type', '')
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
            engine_liters=engine_liters,
            engine_cylinders=engine_cylinders,
            fuel_type=fuel_type,
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

        # Handle image uploads (max 10)
        images = []
        uploaded_files = request.files.getlist('images')
        print(f"DEBUG: Number of files received: {len(uploaded_files)}")
        
        for file in uploaded_files:
            if file and file.filename:
                # Generate unique filename to avoid conflicts
                import uuid
                ext = os.path.splitext(file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(filepath)
                # Store relative path for templates
                images.append(f'uploads/{unique_filename}')
                print(f"DEBUG: Saved image {len(images)}: {unique_filename}")
                
                if len(images) >= 10:
                    break
        
        if images:
            car.set_images(images)
            print(f"DEBUG: Total images saved: {len(images)}")
        
        # Handle video uploads (max 3) - Temporarily disabled until database migrated
        # videos = []
        # for file in request.files.getlist('videos'):
        #     if file and file.filename:
        #         filename = secure_filename(file.filename)
        #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(filepath)
        #         # Store relative path for templates
        #         videos.append(f'uploads/{filename}')
        #         if len(videos) >= 3:
        #             break
        # 
        # if videos:
        #     car.set_videos(videos)

        db.session.add(car)
        db.session.commit()
        flash('Car uploaded successfully!')
        return redirect(url_for('profile'))

    return render_template('upload.html', 
                         features_options=FEATURES_OPTIONS,
                         car_makes=sorted(CAR_MAKES_MODELS.keys()),
                         years=YEARS,
                         categories=CATEGORIES,
                         engine_liters=ENGINE_LITERS,
                         engine_cylinders=ENGINE_CYLINDERS,
                         fuel_types=FUEL_TYPES,
                         gearbox_options=GEARBOX_OPTIONS,
                         steering_options=STEERING_OPTIONS,
                         drive_options=DRIVE_OPTIONS,
                         doors_options=DOORS_OPTIONS,
                         colors=COLORS,
                         interior_materials=INTERIOR_MATERIALS,
                         interior_colors=INTERIOR_COLORS)

@app.route('/profile')
@login_required
def profile():
    cars = current_user.cars.all()
    return render_template('profile.html', cars=cars)

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
@login_required
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)
    
    # Check if user owns this car
    if car.user_id != current_user.id:
        flash('Unauthorized to edit this car')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        # Update basic fields
        car.make = request.form.get('make', '')
        car.model = request.form.get('model', '')
        
        year = request.form.get('year', '0')
        price = request.form.get('price', '0')
        mileage = request.form.get('mileage', '0')
        
        # Safe conversions
        try:
            car.year = int(year) if year else 0
        except ValueError:
            car.year = 0
        
        try:
            car.price = float(price) if price else 0.0
        except ValueError:
            car.price = 0.0
        
        try:
            car.mileage = int(mileage) if mileage else 0
        except ValueError:
            car.mileage = 0
        
        car.engine_liters = request.form.get('engine_liters', '')
        car.engine_cylinders = request.form.get('engine_cylinders', '')
        car.fuel_type = request.form.get('fuel_type', '')
        car.category = request.form.get('category', '')
        car.gearbox = request.form.get('gearbox', '')
        car.steering = request.form.get('steering', '')
        car.drive = request.form.get('drive', '')
        car.doors = request.form.get('doors', '')
        
        tech_inspection_value = request.form.get('tech_inspection', '')
        catalyst_value = request.form.get('catalyst', '')
        car.tech_inspection = tech_inspection_value == 'Yes' if tech_inspection_value else False
        car.catalyst = catalyst_value == 'Yes' if catalyst_value else False
        
        car.color = request.form.get('color', '')
        car.interior_material = request.form.get('interior_material', '')
        car.interior_color = request.form.get('interior_color', '')
        car.description = request.form.get('description', '')
        
        # Update features
        features = request.form.getlist('features')
        if features:
            car.set_features(features)
        
        # Handle new image uploads (max 10)
        new_images = []
        for file in request.files.getlist('images'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                new_images.append(f'uploads/{filename}')
                if len(new_images) >= 10:
                    break
        
        # If new images uploaded, update; otherwise keep existing
        if new_images:
            car.set_images(new_images)
        
        # Handle new video uploads (max 3) - Temporarily disabled until database migrated
        # new_videos = []
        # for file in request.files.getlist('videos'):
        #     if file and file.filename:
        #         filename = secure_filename(file.filename)
        #         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #         file.save(filepath)
        #         new_videos.append(f'uploads/{filename}')
        #         if len(new_videos) >= 3:
        #             break
        # 
        # # If new videos uploaded, update; otherwise keep existing
        # if new_videos:
        #     car.set_videos(new_videos)
        
        db.session.commit()
        flash('Car updated successfully!')
        return redirect(url_for('car_detail', car_id=car.id))
    
    return render_template('edit.html', 
                         car=car,
                         features_options=FEATURES_OPTIONS,
                         car_makes=sorted(CAR_MAKES_MODELS.keys()),
                         car_models=CAR_MAKES_MODELS,
                         years=YEARS,
                         categories=CATEGORIES,
                         engine_liters=ENGINE_LITERS,
                         engine_cylinders=ENGINE_CYLINDERS,
                         fuel_types=FUEL_TYPES,
                         gearbox_options=GEARBOX_OPTIONS,
                         steering_options=STEERING_OPTIONS,
                         drive_options=DRIVE_OPTIONS,
                         doors_options=DOORS_OPTIONS,
                         colors=COLORS,
                         interior_materials=INTERIOR_MATERIALS,
                         interior_colors=INTERIOR_COLORS)

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