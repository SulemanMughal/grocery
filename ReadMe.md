# Frontend

This branch contains the frontend (Next.js) for the Grocery project.

## Getting Started


### Clone this repo and checkout the frontend branch:

```sh
git clone -b frontend https://github.com/SulemanMughal/grocery.git
```

1. Install dependencies:
   ```sh
   npm install
   ```

2. Start the development server:
   ```sh
   npm run dev
   ```
   The app will be available at [http://localhost:3000](http://localhost:3000).

---

### Using Docker

1. **Build and run with Docker Compose:**
   ```sh
   docker compose up -d --build
   ```
   This will build the Docker image and start the frontend server on [http://localhost:3000](http://localhost:3000).

2. **Manual Docker build and run:**
   ```sh
   docker build -t grocery-frontend .
   docker run -p 3000:3000 grocery-frontend
   ```

## Project Structure
- `Dockerfile`: Optimized for Next.js production build
- `docker-compose.yml`: Compose file for easy startup
- `package.json`: Project dependencies
- `public/`: Static assets
- `app/`, `components/`, etc.: Source code

## Environment Variables
You can add environment variables in the `docker-compose.yml` under `environment:` or use a `.env` file as needed.

---

For backend setup, see the `main` branch of this repository.
