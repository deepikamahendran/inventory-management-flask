  
# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# --- Flask Configuration ---
app = Flask(__name__)
# Configure SQLite database (inventory.db file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Secret key for flashing messages (required by Flask)
app.config['SECRET_KEY'] = 'a_very_secret_key_for_inventory'
db = SQLAlchemy(app)

# --- Database Models ---

class Product(db.Model):
    """Represents a product item."""
    product_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Location(db.Model):
    """Represents a storage location/warehouse."""
    location_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Location {self.name}>'

class ProductMovement(db.Model):
    """Tracks movement of products between locations."""
    movement_id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-', ''))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    product_id = db.Column(db.String, db.ForeignKey('product.product_id'), nullable=False)
    # The 'from_location' and 'to_location' can be nullable based on the Note:
    from_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True) # Incoming: blank
    to_location = db.Column(db.String, db.ForeignKey('location.location_id'), nullable=True)     # Outgoing: blank
    
    qty = db.Column(db.Integer, nullable=False)
    
    # Relationships for easier access
    product = db.relationship('Product', backref=db.backref('movements', lazy=True))
    location_from = db.relationship('Location', foreign_keys=[from_location], backref='outgoing_movements')
    location_to = db.relationship('Location', foreign_keys=[to_location], backref='incoming_movements')

    def __repr__(self):
        return f'<Movement {self.movement_id}>'

# --- Utility Functions (for Report) ---

def calculate_inventory_balance():
    """
    Calculates the net balance (Qty) for each Product in each Location.
    
    Incoming movements (+Qty) are tracked via 'to_location'.
    Outgoing movements (-Qty) are tracked via 'from_location'.
    """
    # 1. Incoming Movements (to_location is filled, from_location is optional/null)
    incoming_query = db.session.query(
        Product.name.label('product_name'),
        Location.name.label('location_name'),
        db.func.sum(ProductMovement.qty).label('incoming_qty')
    ).join(Product).join(Location, ProductMovement.to_location == Location.location_id).group_by(Product.name, Location.name).all()
    
    # 2. Outgoing Movements (from_location is filled, to_location is optional/null)
    outgoing_query = db.session.query(
        Product.name.label('product_name'),
        Location.name.label('location_name'),
        db.func.sum(ProductMovement.qty).label('outgoing_qty')
    ).join(Product).join(Location, ProductMovement.from_location == Location.location_id).group_by(Product.name, Location.name).all()
    
    # Consolidate results
    balances = {}

    # Process incoming
    for prod_name, loc_name, qty in incoming_query:
        key = (prod_name, loc_name)
        balances[key] = balances.get(key, 0) + qty

    # Process outgoing
    for prod_name, loc_name, qty in outgoing_query:
        key = (prod_name, loc_name)
        balances[key] = balances.get(key, 0) - qty
        
    # Format for display: List of dictionaries
    report_data = [
        {'product': k[0], 'warehouse': k[1], 'qty': v} 
        for k, v in balances.items() if v != 0 # Only show locations with non-zero inventory
    ]
    
    return report_data

# --- Routes (Views) ---

@app.route('/')
def index():
    """Main page showing the inventory balance report."""
    report_data = calculate_inventory_balance()
    return render_template('index.html', report_data=report_data)

@app.route('/products', methods=['GET', 'POST'])
def manage_products():
    """Add/View Products."""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if not name:
            flash('Product name is required.', 'error')
        else:
            try:
                new_product = Product(name=name, description=description)
                db.session.add(new_product)
                db.session.commit()
                flash(f'Product "{name}" added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding product: {str(e)}', 'error')
        return redirect(url_for('manage_products'))

    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/locations', methods=['GET', 'POST'])
def manage_locations():
    """Add/View Locations."""
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            flash('Location name is required.', 'error')
        else:
            try:
                new_location = Location(name=name)
                db.session.add(new_location)
                db.session.commit()
                flash(f'Location "{name}" added successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding location: {str(e)}', 'error')
        return redirect(url_for('manage_locations'))

    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/movements', methods=['GET', 'POST'])
def manage_movements():
    """Add/View ProductMovements."""
    products = Product.query.all()
    locations = Location.query.all()

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        qty = request.form.get('qty', type=int)
        from_location_id = request.form.get('from_location')
        to_location_id = request.form.get('to_location')
        
        # Validate inputs
        if not product_id or qty is None or qty <= 0:
            flash('Product and a positive Quantity are required.', 'error')
            return redirect(url_for('manage_movements'))
            
        # Ensure at least one location is specified (Incoming OR Outgoing OR Transfer)
        if not from_location_id and not to_location_id:
            flash('Either "From Location" or "To Location" must be selected.', 'error')
            return redirect(url_for('manage_movements'))
            
        # Handle "None" selection from form
        from_location = from_location_id if from_location_id != 'None' else None
        to_location = to_location_id if to_location_id != 'None' else None

        try:
            new_movement = ProductMovement(
                product_id=product_id,
                qty=qty,
                from_location=from_location,
                to_location=to_location
            )
            db.session.add(new_movement)
            db.session.commit()
            flash('Product Movement recorded successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error recording movement: {str(e)}', 'error')
        
        return redirect(url_for('manage_movements'))

    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).limit(50).all() # Show latest 50
    return render_template('movements.html', movements=movements, products=products, locations=locations)

# --- Initializer and Runner ---

@app.cli.command("init-db")
def init_db():
    """Initialize the database and create tables."""
    db.create_all()
    print("Database tables created.")
    
@app.cli.command("seed-data")
def seed_data():
    """Seeds initial products, locations, and movements."""
    db.create_all() # Ensure tables exist
    
    # 1. Create Products
    p1 = Product(name='Laptop Pro', description='High-end laptop model')
    p2 = Product(name='Monitor 27"', description='4K display')
    p3 = Product(name='Keyboard Mech', description='Mechanical Keyboard')
    db.session.add_all([p1, p2, p3])
    db.session.commit()
    print("3 Products created.")
    
    # 2. Create Locations
    l1 = Location(name='Warehouse A')
    l2 = Location(name='Shop Floor')
    l3 = Location(name='Receiving Dock')
    db.session.add_all([l1, l2, l3])
    db.session.commit()
    print("3 Locations created.")
    
    # 3. Make ProductMovements (20 movements for testing)
    movements_data = [
        # Incoming: Move Product A (Laptop Pro) to Location X (Warehouse A)
        {'product': p1.product_id, 'qty': 50, 'to': l1.location_id, 'from': None},
        # Incoming: Move Product B (Monitor) to Location X (Warehouse A)
        {'product': p2.product_id, 'qty': 100, 'to': l1.location_id, 'from': None},
        # Incoming: Move Product A (Laptop Pro) to Location Y (Shop Floor)
        {'product': p1.product_id, 'qty': 10, 'to': l2.location_id, 'from': None},
        # Transfer: Move Product A from Location X (Warehouse A) to Location Y (Shop Floor)
        {'product': p1.product_id, 'qty': 5, 'from': l1.location_id, 'to': l2.location_id},
        # Outgoing/Sale: Move Product A out of Location Y (Shop Floor) (Sale)
        {'product': p1.product_id, 'qty': 1, 'from': l2.location_id, 'to': None},
        # Incoming: Monitor to Shop Floor
        {'product': p2.product_id, 'qty': 5, 'to': l2.location_id, 'from': None},
        # Transfer: Monitor from Warehouse A to Shop Floor
        {'product': p2.product_id, 'qty': 2, 'from': l1.location_id, 'to': l2.location_id},
        # Incoming: Keyboard to Warehouse A
        {'product': p3.product_id, 'qty': 80, 'to': l1.location_id, 'from': None},
        # Transfer: Keyboard from Warehouse A to Receiving Dock
        {'product': p3.product_id, 'qty': 10, 'from': l1.location_id, 'to': l3.location_id},
        # Outgoing: Monitor from Shop Floor
        {'product': p2.product_id, 'qty': 3, 'from': l2.location_id, 'to': None},
        # Remaining 10 for variety and balance
        {'product': p1.product_id, 'qty': 2, 'from': l1.location_id, 'to': l2.location_id},
        {'product': p2.product_id, 'qty': 10, 'from': l1.location_id, 'to': l2.location_id},
        {'product': p3.product_id, 'qty': 5, 'from': l1.location_id, 'to': None},
        {'product': p1.product_id, 'qty': 1, 'from': l2.location_id, 'to': None},
        {'product': p2.product_id, 'qty': 1, 'from': l2.location_id, 'to': None},
        {'product': p1.product_id, 'qty': 20, 'to': l1.location_id, 'from': None},
        {'product': p3.product_id, 'qty': 5, 'to': l3.location_id, 'from': None},
        {'product': p3.product_id, 'qty': 2, 'from': l3.location_id, 'to': None},
        {'product': p2.product_id, 'qty': 5, 'from': l1.location_id, 'to': None},
        {'product': p1.product_id, 'qty': 10, 'from': l1.location_id, 'to': l3.location_id}
    ]

    for data in movements_data:
        movement = ProductMovement(
            product_id=data['product'],
            qty=data['qty'],
            from_location=data['from'],
            to_location=data['to']
        )
        db.session.add(movement)
    
    db.session.commit()
    print(f"{len(movements_data)} Product Movements created (approx 20).")
    print("Data seeding complete.")


if __name__ == '__main__':
    # Initial setup on first run
    with app.app_context():
        # This will create the database file and tables if they don't exist
        db.create_all() 
    app.run(debug=True)