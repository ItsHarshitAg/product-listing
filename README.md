# Product Listing and Checkout System

A simple Django web application that implements a basic Product Listing and Checkout system.

## Live Demo

You can explore the live demo at [product-listing-demo.example.com](https://github.com/yourusername/product-listing) (update with your actual deployment URL when available).

## Features

- Product listing with details (name, description, price, image, stock)
- Product images for all items
- Cart functionality using Django sessions (no login required)
- Add/remove products to/from cart via AJAX
- View cart contents
- Simulate checkout process

## Setup Instructions

1. Clone this repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Create the default admin user (username: admin, password: admin):

   ```bash
   python manage.py create_admin
   ```

5. Populate the database with sample products:

   ```bash
   python manage.py loaddata products
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Access the application at: `http://127.0.0.1:8000/`

## Project Structure

- `product_listing/` - Main project folder
- `shop/` - Django app for the product listing and cart functionality
- `static/` - Static files (CSS, JavaScript)
- `templates/` - HTML templates

## Admin Interface

The application includes a Django admin interface for managing products and inventory:

1. Access the admin panel at: `http://127.0.0.1:8000/admin/`
2. Login credentials:
   - Username: `admin`
   - Password: `admin`

3. Admin features:
   - Add new products with images, descriptions, and pricing
   - Update product stock levels when restocking inventory
   - View and manage product information
   - Monitor product inventory
