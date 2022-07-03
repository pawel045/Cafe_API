from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
API_KEY = '29Cs0kuu9_iIoHg-0W-nZQ'

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


def to_dict(data):

    data_dict = []
    for pos in data:
        pos_dict = dict(pos.__dict__)
        del pos_dict['_sa_instance_state']
        data_dict.append(pos_dict)

    return data_dict


@app.route("/")
def home():

    return render_template("index.html")
    

# HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    cafe = choice(Cafe.query.all())
    cafe_dict = dict(cafe.__dict__)
    del cafe_dict['_sa_instance_state']

    return jsonify(cafe=cafe_dict)


@app.route("/all")
def get_all_cafe():
    cafes_list = Cafe.query.all()
    cafes_dict = to_dict(cafes_list)

    return jsonify(cafe=cafes_dict)


@app.route("/search")
def search():
    location = request.args.get('loc')
    cafes_list = Cafe.query.filter_by(location=location)
    cafes_dict = to_dict(cafes_list)

    if cafes_dict:
        return jsonify(cafe=cafes_dict)
    else:
        return jsonify(cafe='Sorry, we don\'t have cafe in that location.')


# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add_new_cafe():
    new_cafe = Cafe(
        name=request.form.get('name'),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        seats=request.form.get('seats'),
        has_toilet=bool(request.form.get('has_toilet')),
        has_wifi=bool(request.form.get('has_wifi')),
        has_sockets=bool(request.form.get('has_sockets')),
        can_take_calls=bool(request.form.get('can_take_calls')),
        coffee_price=request.form.get('coffee_price'),
    )
    db.session.add(new_cafe)
    db.session.commit()

    return jsonify(response={"success": "Successfully added the new cafe"})


# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def change_price(cafe_id):
    cafe_to_change = Cafe.query.get(cafe_id)
    new_price = request.args.get('new_price')

    if cafe_to_change:
        cafe_to_change.coffee_price = new_price
        db.session.commit()

        return jsonify(response={"success": "Successfully change a coffee price."})

    else:
        return jsonify(error={"Not Found": "Sorry, cafe with that id was not found in database."})


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get('api_key')
    del_cafe = Cafe.query.get(cafe_id)

    if del_cafe:
        if api_key == API_KEY:
            db.session.delete(del_cafe)
            db.session.commit()
            return jsonify(reaposne={"success": "Successfully delete the cafe."})

        else:
            return jsonify(error={"KeyError": "Failed, the api key was wrong"})

    else:
        return jsonify(error={"Not Found": "Sorry, cafe with that id was not found in database."})


if __name__ == '__main__':
    app.run(debug=True)
