📦 Inventory Management System (Flask + SQLAlchemy)
A dedicated web application built on the Flask micro-framework, designed for real-time tracking and management of product stock across multiple storage locations or warehouses. This system provides granular control over inventory movements and generates instantaneous stock balance reports.

✨ Key Features
The application addresses core inventory control requirements through structured data management and reporting.

Category

Feature

Description

Data Integrity

SQLAlchemy ORM

Utilizes robust SQLAlchemy models for Product, Location, and ProductMovement with UUID-based primary keys.

Transaction Control

Movement Logging

Records every stock movement, including incoming, outgoing, and inter-location transfers, logging the timestamp and transaction qty.

Core Functionality

Master Data Management

Dedicated views for professional data entry and listing of Products and Locations.

Reporting

Real-Time Stock Balance

The primary report provides an aggregate view of the net quantity of every product currently held in every defined location/warehouse.

🚀 Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
Python 3.8 or higher

pip (Python package installer)

git (Version control)

Installation and Execution
Clone the Repository:
Retrieve the project files from GitHub.

git clone [https://github.com/deepikamahendran/inventory-management-flask.git](https://github.com/deepikamahendran/inventory-management-flask.git)
cd inventory-management-flask

Install Dependencies:
Install the required Python libraries (Flask, Flask-SQLAlchemy, etc.).

pip install -r requirements.txt

Initialize and Seed Database:
These commands create the necessary local inventory.db file and populate it with sample data (products, locations, and 20 movement transactions) to immediately test the reporting feature.

flask init-db
flask seed-data

Run the Local Server:
Start the Flask development server.

python app.py

The application will be accessible via your browser at http://127.0.0.1:5000.

🖼️ Application Views
The application interface is designed for clarity and easy navigation across key inventory tasks.

1. Inventory Balance Report
The central reporting feature, showcasing the Net Quantity (balance) per product per location.

2. Product Movement Screen
The transaction interface for logging all stock movements (Inbound, Outbound, or Transfer).

3. Products and Locations Management
Views dedicated to defining the core master data used throughout the application.
