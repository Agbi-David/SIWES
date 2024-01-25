from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/database'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    time = db.Column(db.String(100))
    people = db.Column(db.String(100))
    message = db.Column(db.String(500))

# New Menu model for the menu list
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    price = db.Column(db.Float)

# User Cart model
class UserCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100))
    item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'))
    quantity = db.Column(db.Integer)

@app.route('/add_to_cart/<int:item_id>')
def add_to_cart(item_id):
    # For simplicity, assuming user's email is stored in session
    user_email = "user@example.com"
    
    # Check if the item is already in the cart
    existing_item = UserCart.query.filter_by(user_email=user_email, item_id=item_id).first()

    if existing_item:
        existing_item.quantity += 1
    else:
        new_cart_item = UserCart(user_email=user_email, item_id=item_id, quantity=1)
        db.session.add(new_cart_item)

    db.session.commit()

    return redirect(url_for('menu'))

# Route to display the admin menu (CRUD operations)
@app.route('/admin/menu')
def admin_menu():
    menu_items = MenuItem.query.all()
    return render_template('admin_menu.html', menu_items=menu_items)

# Route to add a new menu item
@app.route('/admin/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Extract data from the form and create a new MenuItem
        item_name = request.form.get('item_name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        new_item = MenuItem(item_name=item_name, description=description, price=price)
        
        # Add the new item to the database
        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for('admin_menu'))

    return render_template('add_item.html')  # Create this template for the add item form

# Route to edit an existing menu item
@app.route('/admin/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = MenuItem.query.get(item_id)

    if request.method == 'POST':
        # Update the item's data based on the form submission
        item.item_name = request.form.get('item_name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))

        # Commit the changes to the database
        db.session.commit()

        return redirect(url_for('admin_menu'))

    return render_template('edit_item.html', item=item)  # Create this template for the edit item form

# Route to delete an existing menu item
@app.route('/admin/delete_item/<int:item_id>')
def delete_item(item_id):
    item = MenuItem.query.get(item_id)
    
    # Remove the item from the database
    db.session.delete(item)
    db.session.commit()

    return redirect(url_for('admin_menu'))

# Routes for admins
# @app.route('/admin/menu')
# def admin_menu():
#     menu_items = MenuItem.query.all()
#     return render_template('admin_menu.html', menu_items=menu_items)


@app.route('/home', methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        time = request.form.get('time')
        message = request.form.get('message')
        people = request.form.get('people')
        data = Data(name=name, email=email, time=time, message=message, people=people)
        db.session.add(data)
        db.session.commit()
    return render_template('home.html')


@app.route("/admin")
def admin():
    user_data = Data.query.all()
    return render_template("admin.html", user_data=user_data)

@app.route("/menu")
def menuList():
    user_data = MenuItem.query.all()
    return render_template("menu.html", user_data=user_data)

@app.route("/about")
def aboutUs():
    return render_template("about.html")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


