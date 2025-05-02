# Flashcard Application

A web-based flashcard application built with Flask that helps users create and study flashcards. The application includes user authentication, admin functionality, and flashcard management features.

## Features

- User authentication (login/registration)
- Flashcard creation and management
- Admin dashboard for user management
- Study session tracking
- Responsive web interface

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd flashcard-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///flashcards_log.db
```

5. Initialize the database:
```bash
python database_setup.py
```

6. Run the application:
```bash
python flask_app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

- `flask_app.py`: Main application file
- `database.py`: Database models and setup
- `user_management.py`: User authentication and management
- `flashcard_logic.py`: Flashcard-related functionality
- `templates/`: HTML templates
- `database_setup.py`: Database initialization script

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.