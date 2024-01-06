

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Enable CORS for all routes

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_of_recipe = db.Column(db.String(45), nullable=False)
    ingredients = db.Column(db.String(45), nullable=False)
    prepare_time = db.Column(db.String(45), nullable=False)
    # image = db.Column(db.String(100), nullable=False)


# Uncomment the next two lines to create tables
# with app.app_context():
#     db.create_all()

@app.route('/list_recipes', methods=['GET'])
def list_recipes():
    recipes = Recipe.query.all()
    recipes_list = []
    for recipe in recipes:
        recipes_list.append({
            'id': recipe.id,
            'name_of_recipe': recipe.name_of_recipe,
            'ingredients': recipe.ingredients,
            'prepare_time': recipe.prepare_time
        })
    return jsonify({'recipes': recipes_list})

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    try:
        data = request.get_json()
        new_recipe = Recipe(
            name_of_recipe=data.get('name_of_recipe'),
            ingredients=data.get('ingredients'),
            prepare_time=data.get('prepare_time')
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_recipe/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    try:
        recipe_to_delete = Recipe.query.get(recipe_id)
        if recipe_to_delete:
            db.session.delete(recipe_to_delete)
            db.session.commit()
            return jsonify({'message': 'Recipe deleted successfully'})
        else:
            return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/update_recipe/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        recipe_to_update = Recipe.query.get(recipe_id)
        if recipe_to_update:
            data = request.get_json()
            recipe_to_update.name_of_recipe = data.get('name_of_recipe')
            recipe_to_update.ingredients = data.get('ingredients')
            recipe_to_update.prepare_time = data.get('prepare_time')
            db.session.commit()
            return jsonify({'message': 'Recipe updated successfully'}), 200
        else:
            return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

