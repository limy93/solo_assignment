# EpochCraft: A Sustainable E-commerce Platform for EcoCredits

EpochCraft is an e-commerce platform developed in Python with Django. It sells 'EcoCredits', an imaginative concept designed to contribute directly to global sustainability efforts. This README provides guidelines for setting up, running, and testing the application, as well as how to contribute to its development.

## Prerequisites

- Python 3.10+
- Django 4.1+
- Pyenv (optional, for managing Python versions)

## Setup

### Clone the Repository
First, clone the repository to your local machine:

    git clone git@github.com:limy93/solo_assignment.git
    cd solo_assignment

### Environment Setup
Install Python using 'pyenv' and set up a virtual environment:

    pyenv local 3.10.7   # Set the local version of Python to 3.10.7
    python3 -m venv .venv   # Create a virtual environment
    source .venv/bin/activate   # Activate the virtual environment
    pip install --upgrade pip   # Optional: Upgrade pip
    pip install -r requirements.txt   # Install dependencies

### Database and Data Import
Prepare the database and import initial data:

    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py import_csv_data   # Import data as products

### Simulate Data
Use Faker to generate users (customers) and purchases:

    python3 manage.py populate_data

### Superuser Creation
Create a superuser to access admin features:

    python3 manage.py createsuperuser

### Start the server
Launch the application locally:

    python3 manage.py runserver

This starts the Django development server on localhost using the default port 8000. If you need the server accessible from other devices on your network, or if you need to use a different port, run:

    python3 manage.py runserver 0.0.0.0:8000

Replace 8000 with your desired port number as necessary.

### Accessing the Application
Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or use an appropriate URL to view the application and log in as a superuser to access the Django admin panel.

## Testing

### Django's Built-In Tests
Run Django's built-in tests with:
    
    python3 manage.py test cc_shop.tests

### Behave Tests
Ensure the server is running, then execute Behave tests in a new terminal:

    behave

## Deployment

Access the live application deployed on Render at [https://solo-assignment.onrender.com](https://solo-assignment.onrender.com).

## Contributing

This project is part of a solo assignment and is not currently open for external contributions. If students have suggestions or feedback, they are encouraged to discuss these with their peers or course instructors.

## License

This project is created for educational purposes and is not covered under any specific license.

## Contact

For queries regarding this project, students should contact their course instructors or utilize the academic resources provided by the educational institution.