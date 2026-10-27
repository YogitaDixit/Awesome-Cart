# Awesome Cart — Django E-Commerce Website

Awesome Cart is a web-based e-commerce application built with Django. It provides product browsing, search, cart management, checkout, user accounts, address management, and order tracking.

## Features

- Product listing and product detail pages
- Product search
- Shopping cart
- User registration and login
- Checkout and order placement
- Customer address management
- My Orders page and individual order details
- Order status tracking and progress updates
- Blog section
- Contact page
- Django admin panel for managing application data

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite (development)
- **Version Control:** Git and GitHub

## Project Structure

```text
AwesomeCart/
├── ac/
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── blog/
├── shop/
├── media/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YogitaDixit/Awesome-Cart.git
cd Awesome-Cart
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Django secret key

Set the `DJANGO_SECRET_KEY` environment variable before running the project.

For a temporary Windows PowerShell session, generate a new development key with:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the generated value and set it in PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "paste-generated-key-here"
```

Do not commit secret keys or other credentials to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. If your project uses a different URL route for the home page, use the appropriate route configured in `ac/urls.py`.

## Future Improvements

- Online payment integration
- Product reviews and ratings
- Improved automated testing
- Production deployment

## Author

**Yogita Dixit**

GitHub: [YogitaDixit](https://github.com/YogitaDixit)