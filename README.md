# FastAPI Social Media API

A modern, secure REST API built with FastAPI for a social media platform with user authentication, post management, and voting system.

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Post Management**: Create, read, update, and delete posts with ownership validation
- **Voting System**: Like/unlike posts with vote tracking
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Pydantic models for request/response validation

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Database Migrations**: Alembic
- **API Documentation**: OpenAPI/Swagger
- **Environment Management**: Pydantic Settings

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd fastapi
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
Create a `.env` file in the root directory:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=your_database_name
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 6. Database Setup
1. Create a PostgreSQL database
2. Run Alembic migrations:
```bash
alembic upgrade head
```

### 7. Start the Application
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access:
- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication. To access protected endpoints:

1. **Register a user** using the `/users/` endpoint
2. **Login** using the `/auth/login` endpoint to get an access token
3. **Include the token** in the Authorization header: `Bearer <your_token>`

## 📡 API Endpoints

### Authentication
- `POST /auth/login` - User login (returns JWT token)

### Users
- `POST /users/` - Create a new user
- `GET /users/{id}` - Get user by ID

### Posts
- `GET /posts/` - Get all posts (with pagination and search)
- `POST /posts/` - Create a new post (requires authentication)
- `GET /posts/{id}` - Get a specific post
- `PUT /posts/{id}` - Update a post (requires ownership)
- `DELETE /posts/{id}` - Delete a post (requires ownership)

### Voting
- `POST /vote/` - Vote on a post (like/unlike)

## 🔧 Query Parameters

### Posts Endpoint
- `limit` (int): Number of posts to return (default: 10)
- `skip` (int): Number of posts to skip (default: 0)
- `search` (string): Search posts by content

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `email` (Unique)
- `password` (Hashed)
- `created_at` (Timestamp)

### Posts Table
- `id` (Primary Key)
- `title`
- `content`
- `published` (Boolean)
- `created_at` (Timestamp)
- `owner_id` (Foreign Key to Users)

### Votes Table
- `user_id` (Composite Primary Key)
- `post_id` (Composite Primary Key)

## 🔒 Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **CORS Protection**: Configurable cross-origin resource sharing
- **Input Validation**: All inputs are validated using Pydantic models
- **Ownership Validation**: Users can only modify their own posts

## 🗄️ Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## 🧪 Testing

To run tests (if implemented):
```bash
pytest
```

## 📁 Project Structure

```
fastapi/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py             # Alembic environment
├── app/
│   ├── routers/           # API route handlers
│   │   ├── auth.py        # Authentication routes
│   │   ├── post.py        # Post management routes
│   │   ├── user.py        # User management routes
│   │   └── vote.py        # Voting routes
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── main.py           # FastAPI application
│   ├── models.py         # SQLAlchemy models
│   ├── oauth2.py         # JWT authentication
│   ├── schemas.py        # Pydantic models
│   └── utils.py          # Utility functions
├── venv/                 # Virtual environment
├── alembic.ini          # Alembic configuration
└── README.md            # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues or have questions, please:
1. Check the API documentation at `/docs`
2. Review the error logs
3. Create an issue in the repository

## 🔄 Future Enhancements

- [ ] User profile management
- [ ] Comment system
- [ ] File upload support
- [ ] Email verification
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Unit and integration tests
- [ ] Docker containerization 