# Social Media API

This is a Django REST API for a social media application with user authentication.

## Setup

1. Install dependencies:
   ```
   pip install django djangorestframework django-rest-framework-authtoken Pillow
   ```

2. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Start the server:
   ```
   python manage.py runserver
   ```

## User Model

The custom user model extends Django's AbstractUser with:
- bio: Text field for user biography
- profile_picture: Image field for profile picture
- following: Many-to-many relationship for users this user follows

## Authentication

Uses Django REST Framework's token authentication.

### Register a new user

POST to `/api/register/`

Body:
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "bio": "Optional bio",
    "profile_picture": null
}
```

Response:
```json
{
    "user": {...},
    "token": "token_key"
}
```

### Login

POST to `/api/login/`

Body:
```json
{
    "username": "testuser",
    "password": "password123"
}
```

Response:
```json
{
    "user": {...},
    "token": "token_key"
}
```

### Get/Update Profile

GET/PUT to `/api/profile/`

Requires authentication header: `Authorization: Token <token>`

## Posts and Comments API

### Posts

- **GET /api/posts/**: List all posts (paginated, filterable by author, searchable by title/content)
- **POST /api/posts/**: Create a new post (authenticated users only)
- **GET /api/posts/{id}/**: Retrieve a specific post
- **PUT /api/posts/{id}/**: Update a post (owner only)
- **DELETE /api/posts/{id}/**: Delete a post (owner only)

### Comments

- **GET /api/comments/**: List all comments (paginated, filterable by post/author)
- **POST /api/comments/**: Create a new comment (authenticated users only)
- **GET /api/comments/{id}/**: Retrieve a specific comment
- **PUT /api/comments/{id}/**: Update a comment (owner only)
- **DELETE /api/comments/{id}/**: Delete a comment (owner only)

### Filtering and Pagination

- Pagination: Page-based with 10 items per page
- Post filters: ?author=username, ?search=keyword
- Comment filters: ?post=post_id, ?author=username

### Example Requests

Create a post:
```json
POST /api/posts/
Authorization: Token <token>
{
    "title": "My First Post",
    "content": "This is the content of my post."
}
```

### Follow Management

- **POST /api/follow/<int:user_id>/**: Follow a user (authenticated users only)
- **POST /api/unfollow/<int:user_id>/**: Unfollow a user (authenticated users only)

### Feed

- **GET /api/feed/**: Get posts from followed users (authenticated users only, paginated)

### Example Requests

Follow a user:
```json
POST /api/follow/2/
Authorization: Token <token>
```

Get feed:
```json
GET /api/feed/
Authorization: Token <token>
```

### Likes

- **POST /api/posts/<int:pk>/like/**: Like a post (authenticated users only)
- **POST /api/posts/<int:pk>/unlike/**: Unlike a post (authenticated users only)

### Notifications

- **GET /api/notifications/**: List user's notifications (authenticated users only, paginated)

### Example Requests

Like a post:
```json
POST /api/posts/1/like/
Authorization: Token <token>
```

Get notifications:
```json
GET /api/notifications/
Authorization: Token <token>
```

## Deployment

This application is configured for deployment on Heroku.

### Prerequisites
- Heroku account
- PostgreSQL database (Heroku Postgres recommended)

### Deployment Steps
1. Install Heroku CLI
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
5. Set environment variables:
   - `heroku config:set SECRET_KEY=your-secret-key`
   - `heroku config:set DEBUG=False`
   - `heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com`
6. Push to Heroku: `git push heroku main`
7. Run migrations: `heroku run python manage.py migrate`
8. Collect static files: `heroku run python manage.py collectstatic --noinput`

### Environment Variables
- SECRET_KEY: Django secret key
- DEBUG: False for production
- ALLOWED_HOSTS: Comma-separated list of allowed hosts
- DATABASE_URL: Automatically set by Heroku Postgres

### Local Development
For local development with PostgreSQL, set the database environment variables accordingly.