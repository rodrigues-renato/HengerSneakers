# Henger Sneakers - E-commerce Platform

![Henger Sneakers](templates/static/clientes/img/11039274.jpg)

## Project Overview

Henger Sneakers is a modern e-commerce platform for sneakers, built with Django 5.1. The application allows customers to browse a wide selection of sneakers, create accounts, add items to cart, place orders with multiple payment options, and track their order history. It also includes an administrative dashboard with sales analytics.

## Features

### For Customers
- **User Authentication**: Registration, login, and profile management
- **Product Catalog**: Browse and search sneakers by brand, category, size, and color
- **Shopping Cart**: Add, remove, and modify items in cart
- **Checkout Process**: Multiple payment methods (credit card, debit card, pix, boleto)
- **Address Management**: Save and manage multiple delivery addresses
- **Order History**: View past orders and their details

### For Management
- **Administrative Dashboard**: Visualize sales data with interactive charts
- **Analytics**: 
  - Monthly revenue
  - Total sales
  - Most popular products
  - Monthly customer acquisition
  - Best-selling sneaker models
- **PDF Export**: Export dashboard analytics to PDF format
- **User Management**: Administrative control over user accounts
- **Inventory Control**: Manage product stock levels

## Project Structure

- **clientes**: User authentication and profile management
- **menu**: Product display and cart functionality
- **pedidos**: Order processing and history
- **dashboard**: Analytics and reporting for administrators
- **funcionarios**: Employee management
- **pizzaria**: Core project settings and configuration
- **utils**: Helper functions and utilities

## Technology Stack

- **Backend**: Django 5.1
- **Database**: SQLite (default)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Charts**: Chart.js
- **PDF Generation**: jsPDF, html2canvas
- **Icons**: Font Awesome
- **Image Processing**: Pillow

## Installation

### Requirements
- Python 3.x
- Pip package manager

### Setup

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd pizzaria
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   ```
   
   **Windows**
   ```ps1
   .venv\Scripts\activate
   ```
   **Linux/macOS**
   ```sh
   . .venv/bin/activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (admin):
   ```sh
   python manage.py createsuperuser
   ```

6. Run the server:
   ```sh
   python manage.py runserver
   ```

7. Access the site at [http://localhost:8000](http://localhost:8000)

## Demo Data

To populate the database with demo data, run:

```sh
python utils/create_users.py
python utils/create_products.py
python utils/create_orders.py
```

<!-- ## Screenshots

[Screenshots would be placed here] -->

## Admin Access

The admin interface is available at [http://localhost:8000/admin](http://localhost:8000/admin)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Contributors

- [Renato Rodrigues](https://github.com/rodrigues-renato)
- [Gustavo Giacomini](https://github.com/GustavoGiacomini)
- [Paulo Cesar](https://github.com/paulocjr1)

## Acknowledgements
- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)
- [jsPDF](https://github.com/MrRio/jsPDF)
