```
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

## Project Overview
Full-stack application based on Vue.js 2.x and Flask, providing real-time communication and user management features.

## Tech Stack
- **Frontend**: Vue.js 2.x, Vuex, Vue Router, Element UI, Axios
- **Backend**: Python 3.x, Flask, SQLAlchemy, Flask-SocketIO, Gunicorn

## Project Structure
```
.
├── frontend/                # Vue.js frontend
└── y5-backend-flask/        # Flask backend
    ├── blueprints/        # Blueprint modules
    ├── entity/           # Entity classes
    ├── sql/              # SQL scripts
    ├── app.py           # Main application entry
    ├── config.py        # Configuration
    ├── models.py        # Data models
    └── service.py       # Business logic
```

## Common Commands

### Frontend
```bash
cd frontend
yarn install                # Install dependencies
yarn serve                  # Development server (hot-reload)
yarn build                  # Build for production
```

### Backend
```bash
cd y5-backend-flask
source venv/bin/activate    # Activate virtual environment (Linux/macOS)
# venv\Scripts\activate      # Windows
pip install -r requirements.txt  # Install dependencies
python app.py               # Development server
gunicorn -c gunicorn.py app:app  # Production deployment
```

## Key Files
- `y5-backend-flask/app.py`: Main Flask application entry
- `y5-backend-flask/config.py`: Configuration settings
- `y5-backend-flask/models.py`: SQLAlchemy data models
- `y5-backend-flask/blueprints/`: API endpoints organized by blueprint
- `frontend/src/router/index.js`: Vue Router configuration
- `frontend/src/store/index.js`: Vuex state management

## API Documentation
Available via Swagger UI at: `http://localhost:5000/swagger`