# E-Commerce Backend API

FastAPI-based e-commerce backend with PostgreSQL database.

## Features

- User authentication (JWT)
- Product management
- Shopping cart
- Order management
- Admin endpoints

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT
- **Containerization:** Docker
- **Orchestration:** Kubernetes

## Local Development

### Prerequisites
- Python 3.9+
- PostgreSQL
- Docker & Docker Compose

### Setup

1. Clone the repository
```bash
git clone https://github.com/manideep-itmail/ecommerce-backend.git
cd ecommerce-backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set environment variables
```bash
cp .env.example .env
```

5. Run with Docker Compose (recommended)
```bash
docker-compose up -d
```

6. Run migrations
```bash
alembic upgrade head
```

7. Start server
```bash
uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

## API Endpoints

### Auth
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

### Products
- `GET /api/products` - List all products
- `GET /api/products/{id}` - Get product details
- `POST /api/products` - Create product (Admin)
- `PUT /api/products/{id}` - Update product (Admin)
- `DELETE /api/products/{id}` - Delete product (Admin)

### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/{item_id}` - Update cart item
- `DELETE /api/cart/items/{item_id}` - Remove from cart
- `DELETE /api/cart` - Clear cart

### Orders
- `GET /api/orders` - List user orders
- `POST /api/orders` - Create order from cart
- `GET /api/orders/{id}` - Get order details
- `PUT /api/orders/{id}/status` - Update order status (Admin)

## Docker

### Build
```bash
docker build -t ecommerce-backend:latest .
```

### Run
```bash
docker run -p 8000:8000 ecommerce-backend:latest
```

## Kubernetes

Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
```

## Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## License

MIT
