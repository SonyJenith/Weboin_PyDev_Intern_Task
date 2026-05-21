# TaskFlow - Professional Task Manager

> A full-stack task management application with modern UI, secure authentication, and REST API built with FastAPI and vanilla JavaScript.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

## 📋 Project Overview

TaskFlow is a production-ready task management application designed to help users organize, prioritize, and track their daily tasks. The application features a professional modern UI with no emojis, JWT-based authentication, comprehensive task management capabilities, and pagination.

### Key Features

✅ **Authentication & Security**
- User registration with email validation
- Secure JWT-based authentication
- Password hashing with bcrypt
- CORS protection configured

✅ **Task Management**
- Create, read, update, and delete tasks
- Mark tasks as completed
- Task filtering (All, Pending, Completed)
- Pagination support (10 tasks per page)
- Task descriptions and timestamps

✅ **User Experience**
- Professional, responsive UI design
- Real-time task updates
- Filter tasks by completion status
- Intuitive navigation and controls
- Mobile-friendly layout

✅ **Technical Excellence**
- RESTful API with OpenAPI documentation
- SQLAlchemy ORM with SQLite
- Pydantic validation schemas
- Comprehensive test coverage
- Docker containerization
- Environment-based configuration

## 🏗️ Architecture

### Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend Framework** | FastAPI | 0.104.1 |
| **Web Server** | Uvicorn | 0.24.0 |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Validation** | Pydantic | 2.5.0 |
| **Authentication** | JWT (python-jose) | 3.3.0 |
| **Password Hashing** | bcrypt | 4.0.1 |
| **Database** | SQLite (dev) / PostgreSQL (prod) | - |
| **Frontend** | HTML5/CSS3/JavaScript | - |
| **Testing** | pytest | 7.4.3 |
| **Containerization** | Docker & Docker Compose | latest |

### Project Structure

```
task-manager/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── user.py              # User ORM model
│   │   │   └── task.py              # Task ORM model
│   │   ├── schemas/
│   │   │   ├── user.py              # User validation schemas
│   │   │   └── task.py              # Task validation schemas
│   │   ├── routers/
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   └── tasks.py             # Task CRUD endpoints
│   │   ├── services/
│   │   │   ├── auth_service.py      # Auth business logic
│   │   │   └── task_service.py      # Task business logic
│   │   ├── core/
│   │   │   ├── security.py          # Password & JWT utilities
│   │   │   └── dependencies.py      # Dependency injection
│   │   ├── config.py                # Environment configuration
│   │   ├── database.py              # Database setup
│   │   └── main.py                  # FastAPI app entry point
│   ├── tests/
│   │   ├── conftest.py              # pytest fixtures
│   │   ├── test_auth.py             # Authentication tests
│   │   └── test_tasks.py            # Task CRUD tests
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── .env                         # ⚠️ Never commit this file
├── frontend/
│   ├── index.html                   # Single-page application
│   ├── style.css                    # Professional design system
│   ├── app.js                       # Application logic
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- **Python** 3.11 or higher
- **pip** or **virtualenv**
- **Git** for version control
- **(Optional) Docker** for containerized deployment

### Backend Setup (Local Development)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd task-manager/backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run development server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup (Local Development)

1. **Navigate to frontend:**
   ```bash
   cd ../frontend
   ```

2. **Start HTTP server:**
   ```bash
   # Using Python 3
   python -m http.server 8001

   # Using Node.js (if installed)
   npx http-server -p 8001

   # Using live-server
   live-server --port=8001
   ```

3. **Open in browser:**
   ```
   http://localhost:8001
   ```

## 🔐 Environment Variables

### Required (.env file)

```env
# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=sqlite:///./tasks.db
```

### How to Generate a Secure SECRET_KEY

**Using OpenSSL:**
```bash
openssl rand -base64 32
```

**Using Python:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Production Environment Variables

```env
# Strong secret key (minimum 32 characters)
SECRET_KEY=<very-long-random-string>

# Production database (e.g., PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow

# JWT configuration
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS origins (for production deployment)
CORS_ORIGINS=["https://yourdomain.com","https://app.yourdomain.com"]
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Login User
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "SecurePassword123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Task Endpoints

All task endpoints require the `Authorization: Bearer {token}` header.

#### Create Task
```http
POST /tasks/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Complete project documentation",
  "description": "Write API and user documentation"
}
```

#### Get All Tasks
```http
GET /tasks/?page=1&page_size=10&completed=false
Authorization: Bearer {token}
```

**Response:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete project documentation",
      "description": "Write API and user documentation",
      "completed": false,
      "created_at": "2024-01-01T12:00:00",
      "updated_at": "2024-01-01T12:00:00"
    }
  ],
  "total": 5,
  "page": 1,
  "page_size": 10
}
```

#### Get Specific Task
```http
GET /tasks/{task_id}
Authorization: Bearer {token}
```

#### Update Task
```http
PUT /tasks/{task_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

#### Delete Task
```http
DELETE /tasks/{task_id}
Authorization: Bearer {token}
```

## 🧪 Testing

### Run All Tests
```bash
cd backend
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_auth.py -v
pytest tests/test_tasks.py -v
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
```

### Test Results
- ✅ User registration and validation
- ✅ User login and JWT token generation
- ✅ Task creation with ownership
- ✅ Task filtering and pagination
- ✅ Task completion marking
- ✅ Task updates and deletion
- ✅ Authorization checks
- ✅ Data validation

## 🐳 Docker Deployment

### Build and Run with Docker Compose
```bash
docker-compose up --build
```

This will:
- Start FastAPI backend on port 8000
- Start frontend server on port 3000
- Create and initialize the database

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🌐 Production Deployment

### Environment Setup

1. **Generate secure SECRET_KEY:**
   ```bash
   openssl rand -base64 32
   ```

2. **Set environment variables** in your deployment platform

3. **Update CORS_ORIGINS** to your domain

### Deployment Platforms

#### Render.com (Recommended for Backend)
```bash
# 1. Connect GitHub repository
# 2. Create new Web Service
# 3. Set environment variables:
#    - SECRET_KEY
#    - DATABASE_URL (PostgreSQL)
#    - ALGORITHM
# 4. Build command: pip install -r requirements.txt
# 5. Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### Netlify / Vercel (Frontend)
```bash
# 1. Push frontend to GitHub
# 2. Connect Netlify/Vercel to GitHub
# 3. Set build output directory: frontend/
# 4. Update API_BASE in app.js to production backend URL
# 5. Deploy
```

#### AWS (Complete Stack)
```bash
# Backend: AWS ECS + RDS (PostgreSQL)
# Frontend: AWS S3 + CloudFront
# Alternative: AWS Lambda + API Gateway
```

#### Heroku (Legacy - May Require Credits)
```bash
# Create Procfile:
# web: uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Deploy:
# git push heroku main
```

### Database Migration (Production)

```bash
# For production, use PostgreSQL instead of SQLite

# Update DATABASE_URL in .env:
# DATABASE_URL=postgresql://user:password@host:5432/taskflow

# Databases are auto-initialized on first run
```

## ✅ Security Checklist

- [x] Passwords hashed with bcrypt (salted, not plaintext)
- [x] JWT tokens for stateless authentication
- [x] CORS protection configured
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] XSS prevention (HTML escaping in frontend)
- [x] Secure password validation
- [x] Authentication required on all protected endpoints

### Additional Production Recommendations

- [ ] Enable HTTPS/TLS on all endpoints
- [ ] Implement rate limiting on auth endpoints
- [ ] Add request size limits
- [ ] Enable request logging and monitoring
- [ ] Implement email verification for registration
- [ ] Add password reset functionality
- [ ] Monitor and alert on failed login attempts
- [ ] Regular security audits and updates
- [ ] Implement API versioning
- [ ] Add request tracing and correlation IDs

## 🔧 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'fastapi'"**
```bash
pip install -r requirements.txt
```

**"database is locked"**
```bash
rm backend/tasks.db
# Database will be recreated on next run
```

**"Port 8000 already in use"**
```bash
# Use a different port
uvicorn app.main:app --port 8001 --reload
```

**JWT/Authentication errors**
- Verify `SECRET_KEY` is set in `.env`
- Check token hasn't expired (default: 30 minutes)
- Ensure Authorization header format: `Bearer {token}`

### Frontend Issues

**"Failed to fetch" CORS error**
- Verify backend is running on port 8000
- Check `API_BASE` in `app.js` points to correct backend URL
- Confirm CORS is enabled in backend

**"Port 8001 already in use"**
```bash
python -m http.server 8002  # Use different port
```

**Tasks not loading after login**
- Check browser DevTools console for errors
- Verify JWT token in localStorage
- Confirm backend API is accessible

## 📝 Git Workflow - Clean Commit History

### Initial Setup
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Clean Commit History Strategy

Make logical, atomic commits for each feature/component:

```bash
# 1. Project structure and models
git add backend/app/models/ backend/app/schemas/
git commit -m "feat: add core data models and validation schemas"

# 2. Database and configuration
git add backend/app/database.py backend/app/config.py backend/app/core/
git commit -m "feat: implement database layer and security utilities"

# 3. Authentication system
git add backend/app/routers/auth.py backend/app/services/auth_service.py
git commit -m "feat: add JWT authentication with user registration and login"

# 4. Task management system
git add backend/app/routers/tasks.py backend/app/services/task_service.py
git commit -m "feat: add task CRUD with pagination and filtering"

# 5. API entry point
git add backend/app/main.py
git commit -m "feat: configure FastAPI app with CORS and route integration"

# 6. Test coverage
git add backend/tests/
git commit -m "test: add comprehensive test suite for auth and tasks"

# 7. Frontend UI
git add frontend/
git commit -m "feat: add professional responsive UI with authentication flow"

# 8. Docker configuration
git add Dockerfile docker-compose.yml backend/Dockerfile frontend/Dockerfile
git commit -m "ci: add Docker containerization for development and production"

# 9. Documentation and configuration
git add README.md requirements.txt .env.example .gitignore
git commit -m "docs: add comprehensive documentation and project setup"
```

### Push to Repository

```bash
# Create repository on GitHub first (recommended)

git remote add origin https://github.com/yourusername/task-manager.git
git branch -M main
git push -u origin main

# Verify clean history
git log --oneline --graph
```

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT.io](https://jwt.io/)
- [REST API Best Practices](https://restfulapi.net/)

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** with clear messages: `git commit -m 'feat: add your feature'`
4. **Push** to branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

### Commit Message Convention

```
<type>(<scope>): <subject>

feat:    new feature
fix:     bug fix
docs:    documentation changes
style:   code style changes (formatting)
refactor: code refactoring without feature changes
test:    adding or updating tests
ci:      CI/CD configuration
chore:   build process, dependencies
```

## 🐛 Bug Reports

Found a bug? Please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## 📧 Support

For questions or issues:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and reproduction steps

---

## 🎉 Getting Started

**Ready to use TaskFlow?**

```bash
# Development - Backend
cd backend && python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Development - Frontend (in another terminal)
cd frontend
python -m http.server 8001
# Open http://localhost:8001

# Production with Docker
docker-compose up --build
```

**Built with ❤️ for efficient task management**

---

**Last Updated:** January 2024  
**Version:** 1.0.0  
**Status:** Production Ready ✅
