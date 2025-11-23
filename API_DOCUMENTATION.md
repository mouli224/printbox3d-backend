# PrintBox3D Backend - API Documentation

## Base URL

- **Development**: `http://localhost:8000/api/`
- **Production**: `https://your-domain.railway.app/api/`

## Authentication

The API uses JWT (JSON Web Token) authentication for user-related operations. Some endpoints are public, while others require authentication.

### Public Endpoints
- All product, category, material, and testimonial endpoints
- Contact and newsletter submission endpoints
- User registration and login endpoints

### Protected Endpoints
- User profile endpoints (require JWT token in Authorization header)

### Authentication Header Format
```
Authorization: Bearer <access_token>
```

## Response Format

All API responses follow this format:

**Success Response:**
```json
{
  "count": 10,
  "next": "http://api.example.org/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

## Endpoints

### 1. Products

#### List Products
```
GET /api/products/
```

**Query Parameters:**
- `category__slug` (string): Filter by category slug
- `material__name` (string): Filter by material name
- `is_featured` (boolean): Filter featured products
- `search` (string): Search in product name and description
- `ordering` (string): Sort by field (price, -price, name, -name, created_at, -created_at)
- `page` (integer): Page number for pagination

**Example Request:**
```bash
GET /api/products/?category__slug=home-decor&ordering=price&page=1
```

**Example Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Geometric Planter",
      "slug": "geometric-planter",
      "price": "899.00",
      "image": "/media/products/geometric_planter.jpg",
      "category_name": "Home Decor",
      "material_name": "PLA",
      "is_featured": true,
      "is_available": true,
      "stock_quantity": 10
    }
  ]
}
```

#### Get Product Detail
```
GET /api/products/{slug}/
```

**Example Response:**
```json
{
  "id": 1,
  "name": "Geometric Planter",
  "slug": "geometric-planter",
  "description": "A modern geometric planter perfect for succulents...",
  "price": "899.00",
  "category": {
    "id": 1,
    "name": "Home Decor",
    "slug": "home-decor",
    "description": "Decorative items for your home",
    "image": "/media/categories/home-decor.jpg",
    "product_count": 5,
    "created_at": "2024-01-01T00:00:00Z"
  },
  "material": {
    "id": 1,
    "name": "PLA",
    "description": "Standard biodegradable 3D printing material",
    "properties": "Easy to print, biodegradable, low warping"
  },
  "color": "White",
  "dimensions": "12cm x 12cm x 10cm",
  "weight": "150.00",
  "image": "/media/products/geometric_planter.jpg",
  "image_2": "/media/products/geometric_planter_2.jpg",
  "image_3": null,
  "stock_quantity": 10,
  "is_available": true,
  "is_featured": true,
  "meta_description": "Modern geometric planter for your home",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### Get Featured Products
```
GET /api/products/featured/
```

Returns up to 6 featured products.

#### Get Best Sellers
```
GET /api/products/best_sellers/
```

Returns up to 6 best-selling products.

---

### 2. Categories

#### List Categories
```
GET /api/categories/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Home Decor",
    "slug": "home-decor",
    "description": "Decorative items for your home",
    "image": "/media/categories/home-decor.jpg",
    "product_count": 5,
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Category Detail
```
GET /api/categories/{slug}/
```

---

### 3. Materials

#### List Materials
```
GET /api/materials/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "PLA",
    "description": "Standard biodegradable 3D printing material",
    "properties": "Easy to print, biodegradable, low warping"
  },
  {
    "id": 2,
    "name": "ABS",
    "description": "Durable engineering plastic",
    "properties": "Strong, impact resistant, heat resistant"
  }
]
```

---

### 4. Custom Orders

#### Submit Custom Order
```
POST /api/custom-orders/
```

**Content-Type:** `multipart/form-data`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+91 1234567890",
  "material": "PLA",
  "color": "Blue",
  "description": "I need a custom trophy for my sports event...",
  "quantity": 5,
  "budget": "5000-10000",
  "design_file": "<file upload>"
}
```

**Accepted File Formats:**
- .stl, .obj, .3mf, .step, .stp (3D files)
- .jpg, .jpeg, .png (images)
- .pdf (documents)

**Max File Size:** 10MB

**Response:**
```json
{
  "message": "Custom order request submitted successfully! We will contact you within 24-48 hours.",
  "order_id": 1
}
```

**Validation Errors:**
```json
{
  "design_file": [
    "File size cannot exceed 10MB"
  ]
}
```

---

### 5. Contact Messages

#### Submit Contact Message
```
POST /api/contact/
```

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Product Inquiry",
  "message": "I would like to know more about your custom printing services..."
}
```

**Response:**
```json
{
  "message": "Thank you for contacting us! We will respond within 24 hours.",
  "message_id": 1
}
```

---

### 6. Newsletter

#### Subscribe to Newsletter
```
POST /api/newsletter/
```

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "message": "Successfully subscribed to our newsletter!",
  "email": "john@example.com"
}
```

**Error (Already Subscribed):**
```json
{
  "email": [
    "This email is already subscribed to our newsletter."
  ]
}
```

---

### 7. User Authentication

#### Register User
```
POST /api/auth/register/
```

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Required Fields:**
- `username` (string): Unique username
- `email` (string): Valid email address (unique)
- `password` (string): Strong password (min 8 characters)
- `password2` (string): Password confirmation

**Optional Fields:**
- `first_name` (string)
- `last_name` (string)

**Success Response (201):**
```json
{
  "message": "User registered successfully!",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Validation Errors (400):**
```json
{
  "username": ["A user with that username already exists."],
  "email": ["This email is already registered."],
  "password": ["This password is too common."]
}
```

---

#### Login User
```
POST /api/auth/login/
```

**Content-Type:** `application/json`

**Request Body (Email):**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**OR (Username):**
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Success Response (200):**
```json
{
  "message": "Login successful!",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Error Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

---

#### Refresh Access Token
```
POST /api/auth/token/refresh/
```

**Content-Type:** `application/json`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

#### Get User Profile
```
GET /api/auth/profile/
```

**Authentication:** Required (Bearer token)

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

---

#### Update User Profile
```
PUT /api/auth/profile/update/
```

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@example.com"
}
```

**Response:**
```json
{
  "message": "Profile updated successfully!",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john.smith@example.com",
    "first_name": "John",
    "last_name": "Smith"
  }
}
```

---

#### Logout
```
POST /api/auth/logout/
```

**Authentication:** Required (Bearer token)

**Response:**
```json
{
  "message": "Logout successful!"
}
```

**Note:** Client should discard stored tokens after logout.

---

### 8. Testimonials

#### List Testimonials
```
GET /api/testimonials/
```

**Example Response:**
```json
[
  {
    "id": 1,
    "name": "Jane Smith",
    "company": "Tech Startup Inc.",
    "rating": 5,
    "message": "PrintBox3D delivered exceptional quality. Highly recommended!",
    "image": "/media/testimonials/jane-smith.jpg",
    "created_at": "2024-01-01T00:00:00Z"
  }
]
```

#### Get Featured Testimonials
```
GET /api/testimonials/featured/
```

Returns up to 6 featured testimonials.

---

## Error Codes

- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **400 Bad Request**: Validation error or malformed request
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting for production using Django Rest Framework throttling.

---

## CORS

CORS is configured to allow requests from:
- `http://localhost:3000` (development)
- Your production frontend domain

Update `CORS_ALLOWED_ORIGINS` in settings for additional domains.

---

## Frontend Integration Examples

### Register User

```javascript
const API_URL = 'http://localhost:8000/api';

async function registerUser(userData) {
  const response = await fetch(`${API_URL}/auth/register/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: userData.username,
      email: userData.email,
      password: userData.password,
      password2: userData.password2,
      first_name: userData.firstName,
      last_name: userData.lastName,
    }),
  });
  
  if (response.ok) {
    const data = await response.json();
    // Store tokens in localStorage
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    return data;
  } else {
    const errors = await response.json();
    throw new Error(JSON.stringify(errors));
  }
}
```

### Login User

```javascript
async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });
  
  if (response.ok) {
    const data = await response.json();
    // Store tokens in localStorage
    localStorage.setItem('access_token', data.tokens.access);
    localStorage.setItem('refresh_token', data.tokens.refresh);
    return data;
  } else {
    const error = await response.json();
    throw new Error(error.error || 'Login failed');
  }
}
```

### Fetch User Profile (Authenticated)

```javascript
async function getUserProfile() {
  const token = localStorage.getItem('access_token');
  
  const response = await fetch(`${API_URL}/auth/profile/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (response.ok) {
    return await response.json();
  } else {
    throw new Error('Failed to fetch profile');
  }
}
```

### Refresh Access Token

```javascript
async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch(`${API_URL}/auth/token/refresh/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh: refreshToken }),
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access);
    return data.access;
  } else {
    // Refresh token expired, redirect to login
    localStorage.clear();
    window.location.href = '/login';
  }
}
```

### Fetch Products

```javascript
async function fetchProducts() {
  const response = await fetch(`${API_URL}/products/?is_featured=true`);
  const data = await response.json();
  return data.results;
}
```

### Submit Custom Order

```javascript
async function submitCustomOrder(formData) {
  const response = await fetch(`${API_URL}/custom-orders/`, {
    method: 'POST',
    body: formData, // FormData object with files
  });
  
  if (response.ok) {
    const result = await response.json();
    alert(result.message);
  } else {
    const errors = await response.json();
    console.error(errors);
  }
}
```

### Subscribe to Newsletter

```javascript
async function subscribeNewsletter(email) {
  const response = await fetch(`${API_URL}/newsletter/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email }),
  });
  
  const result = await response.json();
  return result;
}
```

---

## Admin Panel

Access the admin panel at `/admin/` to:
- Manage products, categories, materials
- Review custom orders and update status
- View contact messages
- Manage newsletter subscriptions
- Add/edit testimonials

---

## Database Information

### Connection Details
- **Local Development**: SQLite (automatic)
- **Production**: Supabase PostgreSQL with connection pooling
- **Migrations**: Uses direct connection (bypasses PgBouncer)

### Migration Commands
```bash
# Local development
python manage.py migrate

# Railway/Production (automatic on deploy)
# Uses DIRECT_DATABASE_URL for migrations
# Uses DATABASE_URL for normal operations
```

For complete deployment guide, see **[SUPABASE_RAILWAY_DEPLOYMENT.md](./SUPABASE_RAILWAY_DEPLOYMENT.md)**

---

**Last Updated:** November 2025
