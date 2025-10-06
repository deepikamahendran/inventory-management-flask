📦 Inventory Management System (Flask + SQLAlchemy)

This is a web application built with Python's Flask framework for managing product inventory across various locations (warehouses). It tracks all movements to provide a real-time stock balance report.

## 🌟 Features

* **Database Schema:** Uses SQLAlchemy models for Products, Locations, and ProductMovements.
* **Data Entry:** Dedicated views for creating Products, Locations, and Movements (Incoming, Outgoing, Transfer).
* **Real-time Reporting:** Calculates the net balance (quantity) of every product in every location.

## 🛠️ Setup and Running the Application

### Prerequisites

* Python 3.8+
* `pip` (Python package installer)

### Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourUsername/inventory-management-flask.git](https://github.com/YourUsername/inventory-management-flask.git)
    cd inventory-management-flask
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize and Seed Database:**
    These commands create the required SQLite database file and populate it with test data (3 Products, 3 Locations, and 20 Movements).
    ```bash
    flask init-db
    flask seed-data
    ```
4.  **Run the Server:**
    ```bash
    python app.py
    ```
    The application will be accessible at `http://127.0.0.1:5000`.

## 📸 Application Views

### 1. Inventory Balance Report
(Home Page) Shows the core report: Product, Warehouse, and Net Qty.

![Screenshot of Inventory Balance Report](assets/report_balance.png)

### 2. Product Movement Screen
Form used to record In, Out, or Transfer transactions.

![Screenshot of Product Movement Screen](assets/movement_view.png)

### 3. Products and Locations Management
Screens for defining masters data.

![Screenshot of Products and Locations Screens](assets/products_locations_view.png)"# inventory-management-flask" 
