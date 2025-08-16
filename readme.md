# FlatZ AI

A web application for personalized recommendations powered by AI. Users can sign up, log in, and view a tailored feed. The backend uses FastAPI and stores user and recommendation data in CSV files and a PostgreSQL database.

## Features

- User authentication (sign up, login, logout)
- Personalized feed and recommendations
- Static and template-based frontend
- Data stored in CSV and PostgreSQL (SQLAlchemy models included)

## Project Structure

```
.env
index.html
profile.html
requirements.txt
script.js
style.css
backend/
    auth.py
    database.py
    main.py
    models.py
    recommendations.py
    schemas.py
    data/
        interactions.csv
        items.csv
        users.csv
data/
    users.csv
static/
    2815428.png
    script.js
    style.css
templates/
    feed.html
    index.html
    login.html
    signup.html
```

## Setup

1. **Clone the repository**

   ```sh
   git clone <repo-url>
   cd <project-folder>
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Edit the [`.env`](.env) file with your database credentials.

4. **Run the backend**

   ```sh
   uvicorn backend.main:app --reload
   ```

5. **Access the app**

   Open [http://localhost:8000](http://localhost:8000) in your browser.

## Usage

- Sign up or log in to access your personalized feed.
- View recommendations and profile information.
- Static assets are served from the `/static` directory.

## Data Files

- User, item, and interaction data are stored in CSV files in [`backend/data/`](backend/data).
- Additional user data is in [`data/users.csv`](data/users.csv).

## API Endpoints

- `/api/feed` – Returns feed items (JSON)
- `/login`, `/signup`, `/feed` – HTML pages for authentication and feed