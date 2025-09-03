
# Grocery Project Setup Guide

This guide will help you configure and run the initial setup for the Grocery Django project.

## Prerequisites
- Python 3.8+
- pip
- (Optional) Virtual environment tool (venv, virtualenv, or conda)

## Initial Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/SulemanMughal/grocery -b main
   cd grocery
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in the required values:
     ```bash
     cp grocery/.env.example grocery/.env
     ```
   - Edit `grocery/.env` and set your own values for:

5. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py create_superadmin --email example@example.com --password "example@ss!"
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Visit `http://127.0.0.1:8000/api/doc/` in your browser.

## Docker Setup (Alternative)

For Docker-based development:

1. **Start services with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Default Admin Credentials**
   The system automatically creates a superadmin user with the following credentials:
   - **Email**: `admin@example.com`
   - **Password**: `StrongP@ss!`

   Use these credentials to log in via the API endpoints.

3. **Access the application**
   - API: `http://localhost:8000/api/doc`
   - Neo4j Browser: `http://localhost:7474/`


## API Usage Examples

For ready-to-use API request examples (login, CRUD operations, etc.), see the [`curls.md`](./curls.md) file in this repository.

This file contains:
- Example curl commands for authentication, grocery and supplier management, item operations, and daily income endpoints.
- Consistent formatting and placeholders for easy copy-paste and customization.
- Usage patterns for both admin and supplier roles.

Refer to `curls.md` whenever you need to test or integrate with the API using command-line requests.


## Additional Notes
- For production, set `DEBUG=False` and configure `ALLOWED_HOSTS` properly.
- Store your `.env` file securely and never commit it to version control.
- Refer to Django documentation for further customization.

---

For any issues, please contact the project maintainer.
