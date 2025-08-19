# Django CRM Project

## What This Project Does

This is a simple Customer Relationship Management (CRM) system built with Django. It helps businesses keep track of their customers and their information in one place.

## Features

- User registration and login
- Add new customer records
- View all customer records in a table
- Update existing customer information
- Delete customer records
- Simple and clean web interface

## What You Can Store

For each customer, you can save:
- First name and last name
- Email address
- Phone number
- Complete address (address, city, state, zipcode)
- When the record was created

## Technologies Used

- Python
- Django web framework
- MySQL database
- HTML templates with Bootstrap for styling
- Django forms for user input

## How It Works

1. **Login System**: Users need to register and login to use the CRM
2. **Home Page**: Shows all customer records in a table format
3. **Add Records**: Users can add new customers with their details
4. **View Records**: Click on any customer to see their full information
5. **Update Records**: Edit existing customer information
6. **Delete Records**: Remove customers from the database

## File Structure

The project has these main parts:
- `models.py`: Defines how customer data is stored
- `views.py`: Contains the logic for different pages
- `forms.py`: Handles user forms for registration and adding records
- `templates/`: HTML files for the web pages
- `urls.py`: Maps web addresses to different pages

## Getting Started

1. Clone this repository
2. Install Python and Django
3. Set up MySQL database
4. Run the database setup script: `python mydb.py`
5. Start the Django server: `python manage.py runserver`
6. Open your web browser and go to `localhost:8000`

## Database Setup

The project uses MySQL database named 'elderco'. Make sure you have MySQL installed and update the database settings in `settings.py` with your database credentials.

## Learning Outcomes

This project helped me learn:
- Django basics and how web frameworks work
- Working with databases and models
- Creating forms and handling user input
- User authentication and sessions
- HTML templating and Bootstrap styling
- Basic web development concepts

This is my first Django project and shows the basics of building a web application that can store and manage customer information.
