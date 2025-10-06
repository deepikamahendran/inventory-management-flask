# 📦 Inventory Management System (Flask + SQLAlchemy)
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

🖼️ Application Views
The application interface is designed for clarity and easy navigation across key inventory tasks.

1. Inventory Balance Report
The central reporting feature, showcasing the Net Quantity (balance) per product per location.

2. Product Movement Screen
The transaction interface for logging all stock movements (Inbound, Outbound, or Transfer).

3. Products and Locations Management
Views dedicated to defining the core master data used throughout the application.
