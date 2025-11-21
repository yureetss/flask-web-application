Project Overview

This is a Flask-based web application that provides user authentication, personal account management, and the ability to create posts.
Users can register, log in, manage their profile, upload an avatar, and create their own entries.

The project uses a Blueprint-based structure, Jinja2 templates, SQLAlchemy for database interaction, and Bootstrap for the UI.

Features
Authentication

User registration with database storage.

Login system with session handling.

Access protection for authenticated-only pages.

User Dashboard

Display of profile information: username, email, registration date, number of posts.

Avatar selection from one of four predefined images.

Current avatar preview.

Button to create new posts.

Posts

Creation of user posts.

Viewing personal posts.

Commeting.

Technologies Used

Python 3.10+

Flask

Flask-SQLAlchemy

Jinja2

Bootstrap 5

Werkzeug (secure filename handling)

SQLite or any other SQL database
