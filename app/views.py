#!flask/bin/python
# -*- coding: utf-8 -*

from datetime import datetime
from flask import jsonify, abort, make_response, request
from flask import g, url_for, render_template
from app import app, db, auth
from .models import User, Car, Refill
from config import DATETIME_FMT


def parse_ymd_hms(s):
    ymd, hms = s.split(' ')
    year_s, month_s, day_s = ymd.split('-')
    hour_s, minute_s, second_s = hms.split(':')
    return datetime(int(year_s), int(month_s), int(day_s),
                    int(hour_s), int(minute_s), int(second_s))


@auth.verify_password
def verify_pawwsord(username_or_token, password):
    # Try to authenticate with token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # Try to authenticate with username
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    app.logger.debug("Show index page")
    return render_template("index.html")


@app.route('/carbu/api/v1.0/refills', methods=['GET'])
# @auth.login_required
def get_refills():
    """Get the refills."""
    app.logger.debug('Get refills.')

    car_id = request.args.get('car_id', '')
    app.logger.debug('get_refills: Car_id="%s".', car_id)

    car = Car.query.get(car_id)
    if car is None:
        app.logger.warn('Refill: invalid car parameter "%s".', car_id)
        abort(404)

    refills = []
    for refill in Refill.query.filter_by(car_id=car_id).all():
        app.logger.debug('Refill: %s.', refill.id)
        new_refill = make_public_refill(refill)
        refills.append(new_refill)

    return jsonify(refills=refills)


@app.route('/carbu/api/v1.0/refills/<int:refill_id>', methods=['GET'])
# @auth.login_required
def get_refill(refill_id):
    """Get the refill pointed by the id in parameter."""
    app.logger.debug('Get refill id=%s', refill_id)
    refill = Refill.query.get(refill_id)
    if refill is None:
        abort(404)

    return jsonify(refill=refill.serialize)


@app.route('/carbu/api/v1.0/refills', methods=['POST'])
# @auth.login_required
def create_refill():
    """Create a refill object."""
    app.logger.debug('Create refill.')
    if not request.json:
        abort(400)

    car_id = request.json.get('car_id')
    dt = request.json.get('datetime')
    price = request.json.get('price')
    quantity = request.json.get('quantity')
    mileage = request.json.get('mileage')

    if car_id is None:
        app.logger.debug("No car")
        abort(400)
    else:
        car = Car.query.get(car_id)
        if car is None:
            app.logger.warn("car unknown for id=%s", car_id)
            abort(400)

    if datetime is None:
        app.logger.debug("No datetime")
        abort(400)
    if price is None:
        app.logger.debug("No price")
        abort(400)
    if quantity is None:
        app.logger.debug("No quantity")
        abort(400)
    if mileage is None:
        app.logger.debug("No mileage")
        abort(400)

    refill = Refill(car_id=car_id,
                    datetime=dt,
                    mileage=mileage,
                    price=price,
                    quantity=quantity)

    db.session.add(refill)
    db.session.commit()

    return jsonify({'id': refill.id,
                    'car_id': refill.car_id,
                    'datetime': refill.datetime,
                    'mileage': refill.mileage,
                    'quantity': refill.quantity,
                    'price': refill.price,
                    }), 201


@app.route('/carbu/api/v1.0/refills/<int:refill_id>', methods=['PUT'])
# @auth.login_required
def update_refill(refill_id):
    """Update the refill with the id in parameter."""
    app.logger.debug('Update refill id=%s.', refill_id)
    refill = Refill.query.get(refill_id)
    app.logger.debug('Refill query return %r ' % refill)
    if not refill:
        app.logger.debug('No refill found for id=%s.', refill_id)
        abort(400)

    if not request.json:
        app.logger.debug('No json request.', refill_id)
        abort(400)

    car_id = request.json.get('car_id')
    dt = request.json.get('datetime')
    price = request.json.get('price')
    quantity = request.json.get('quantity')
    mileage = request.json.get('mileage')

    if car_id is None:
        app.logger.debug("No car")
        abort(400)
    else:
        car_id = int(car_id)
        app.logger.debug('Car id =%s', car_id)
        car = Car.query.get(car_id)
        if not car:
            app.logger.error('Car not found for id %s', car_id)
            abort(400)
        if car_id != refill.car_id:
            app.logger.error('car_id is different from the original')
            abort(400)

    if dt is None:
        app.logger.debug("No datetime")
        abort(400)
    else:
        dt = parse_ymd_hms(dt)

    if price is None:
        app.logger.debug("No price")
        abort(400)
    else:
        app.logger.debug('Price %s.', price)
        price = float(price)
        if price < 0.0:
            app.logger.error('Price %s negative !', price)

    if quantity is None:
        app.logger.error('Quantity error.')
        abort(400)
    else:
        app.logger.debug('Quantity %s.', quantity)
        quantity = float(quantity)
        if quantity < 0.0:
            app.logger.error('Quantity %s negative !', quantity)

    if mileage is None:
        app.logger.debug('Mileage error.')
        abort(400)
    else:
        app.logger.debug('Mileage %s.', mileage)
        mileage = int(mileage)
        if mileage < 0:
            app.logger.error('Mileage %s negative !', mileage)

    app.logger.debug('Update refill.[ %s %s %s %s %s ]',
                     car_id, dt, mileage, price, quantity)
    refill.car = car
    refill.datetime = dt
    refill.mileage = mileage
    refill.price = price
    refill.quantity = quantity

    db.session.add(refill)
    db.session.commit()
    return jsonify({'refill': make_public_refill(refill)})


@app.route('/carbu/api/v1.0/refills/<int:refill_id>', methods=['DELETE'])
def delete_refill(refill_id):
    """Delete the refill with the id in parameter."""
    app.logger.debug('Delete refill id=%s.', refill_id)
    refill = Refill.query.get(refill_id)
    app.logger.debug('Refill query return %r ' % refill)
    if not refill:
        app.logger.debug('No refill found for id=%s.', refill_id)
        abort(400)

    db.session.delete(refill)
    db.session.commit()
    return jsonify({'result': True})


def make_public_refill(refill):
    """Replace the id of a refill with an uri to provide direct access."""
    new_refill = {}
    new_refill['uri'] = url_for('get_refill', refill_id=refill.id,
                                _external=True)
    new_refill['car_id'] = refill.car_id
    new_refill['mileage'] = refill.mileage
    new_refill['quantity'] = refill.quantity
    new_refill['price'] = refill.price
    new_refill['datetime'] = refill.datetime.strftime(DATETIME_FMT)
    return new_refill


@app.route('/carbu/api/v1.0/cars', methods=['GET'])
# @auth.login_required
def get_cars():
    """Get the cars."""
    cars = Car.query.all()
    car_cols = ['id', 'name', 'description']
    return jsonify({'cars': [{col: getattr(d, col) for col in car_cols}
                             for d in cars]})


@app.route('/carbu/api/v1.0/cars/<int:car_id>', methods=['GET'])
# @auth.login_required
def get_car(car_id):
    """Get the car pointed by the id in parameter."""
    car = Car.query.get(car_id)
    if not car:
        abort(400)
    return jsonify({'id': car.id,
                    'name': car.name,
                    'description': car.description})


def make_public_car(car):
    """Replace the id of a car with an uri to provide direct access."""
    new_car = {}
    for field in car:
        if field == 'id':
            new_car['uri'] = url_for('get_car', car_id=car['id'],
                                     _external=True)
        else:
            new_car[field] = car[field]
    return new_car


@app.route('/carbu/api/v1.0/users', methods=['POST'])
def new_user():
    """Create a user."""
    if not request.json:
        abort(400)
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None and password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # Duplicate user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'username': user.username}), 201, {'Location':
                                            url_for('get_user',
                                                    user_id=user.id,
                                                    _external=True)}


@app.route('/carbu/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get the user pointed by the id in parameter."""
    user = User.query.get(user_id)
    if not user:
        app.logger.error("Invalid user id %s requested", user_id)
        abort(400)
    return jsonify({'username': user.username})


@app.route('/carbu/api/v1.0/token')
@auth.login_required
def get_auth_token():
    """Get the token generated for the user."""
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})
