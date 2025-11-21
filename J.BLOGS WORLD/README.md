# WriteSphere (Human-style Full Django Blog Scaffold)

This is a human-like, realistic Django blog project scaffold made for portfolio use.
It includes multiple templates, static assets (CSS/JS/images), auth, CRUD, comments, likes, tags, categories, and profiles.

## Quick start (local)
1. Create & activate virtualenv
   - Windows:
     python -m venv venv
     venv\Scripts\activate
   - macOS/Linux:
     python -m venv venv
     source venv/bin/activate

2. Install dependencies
   pip install -r requirements.txt

3. Copy `.env.example` to `.env` (optional) and set SECRET_KEY if desired.

4. Run migrations and create superuser
   python manage.py migrate
   python manage.py createsuperuser

5. Run server
   python manage.py runserver

Open http://127.0.0.1:8000/

-- Notes --
- Uses SQLite by default for easy local testing.
- Includes a custom logout view (works via GET) to match expected UX for portfolio demos.
- Username validation allows international characters (1-50 chars).
