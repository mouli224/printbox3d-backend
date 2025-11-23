# Frontend Integration Guide

## Connecting React Frontend to Django Backend

This guide shows you how to integrate your PrintBox3D React frontend with the Django backend.

## 🔗 Step 1: Update API Configuration

Create a new file `src/config/api.js` in your React project:

```javascript
// src/config/api.js

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const API_ENDPOINTS = {
  // Products
  products: `${API_BASE_URL}/products/`,
  productDetail: (slug) => `${API_BASE_URL}/products/${slug}/`,
  featuredProducts: `${API_BASE_URL}/products/featured/`,
  bestSellers: `${API_BASE_URL}/products/best_sellers/`,
  
  // Categories
  categories: `${API_BASE_URL}/categories/`,
  categoryDetail: (slug) => `${API_BASE_URL}/categories/${slug}/`,
  
  // Materials
  materials: `${API_BASE_URL}/materials/`,
  
  // Forms
  customOrder: `${API_BASE_URL}/custom-orders/`,
  contact: `${API_BASE_URL}/contact/`,
  newsletter: `${API_BASE_URL}/newsletter/`,
  
  // Testimonials
  testimonials: `${API_BASE_URL}/testimonials/`,
  featuredTestimonials: `${API_BASE_URL}/testimonials/featured/`,
};

export default API_BASE_URL;
```

## 🛠️ Step 2: Create API Service

Create `src/services/api.js`:

```javascript
// src/services/api.js
import { API_ENDPOINTS } from '../config/api';

class APIService {
  // Fetch with error handling
  async fetchData(url, options = {}) {
    try {
      const response = await fetch(url, options);
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'API request failed');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // Get products with filters
  async getProducts(filters = {}) {
    const params = new URLSearchParams(filters);
    const url = `${API_ENDPOINTS.products}?${params.toString()}`;
    return this.fetchData(url);
  }

  // Get single product by slug
  async getProduct(slug) {
    return this.fetchData(API_ENDPOINTS.productDetail(slug));
  }

  // Get featured products
  async getFeaturedProducts() {
    return this.fetchData(API_ENDPOINTS.featuredProducts);
  }

  // Get categories
  async getCategories() {
    return this.fetchData(API_ENDPOINTS.categories);
  }

  // Get materials
  async getMaterials() {
    return this.fetchData(API_ENDPOINTS.materials);
  }

  // Submit custom order
  async submitCustomOrder(formData) {
    return this.fetchData(API_ENDPOINTS.customOrder, {
      method: 'POST',
      body: formData, // FormData object
    });
  }

  // Submit contact form
  async submitContact(data) {
    return this.fetchData(API_ENDPOINTS.contact, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  }

  // Subscribe to newsletter
  async subscribeNewsletter(email) {
    return this.fetchData(API_ENDPOINTS.newsletter, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
  }

  // Get testimonials
  async getTestimonials() {
    return this.fetchData(API_ENDPOINTS.testimonials);
  }

  // Get featured testimonials
  async getFeaturedTestimonials() {
    return this.fetchData(API_ENDPOINTS.featuredTestimonials);
  }
}

export default new APIService();
```

## 📝 Step 3: Update Environment Variables

Create/update `.env` in your React project root:

```env
# Development
REACT_APP_API_URL=http://localhost:8000/api

# Production (update after deploying backend)
# REACT_APP_API_URL=https://your-app.railway.app/api
```

## 🔄 Step 4: Update Components

### Shop Page Example

```javascript
// src/pages/Shop/Shop.js
import React, { useState, useEffect } from 'react';
import APIService from '../../services/api';
import './Shop.css';

const Shop = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedMaterial, setSelectedMaterial] = useState('all');

  useEffect(() => {
    fetchProducts();
  }, [selectedCategory, selectedMaterial]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const filters = {};
      if (selectedCategory !== 'all') {
        filters.category__slug = selectedCategory;
      }
      if (selectedMaterial !== 'all') {
        filters.material__name = selectedMaterial;
      }

      const data = await APIService.getProducts(filters);
      setProducts(data.results);
    } catch (error) {
      console.error('Error fetching products:', error);
      alert('Failed to load products. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading products...</div>;
  }

  return (
    <div className="shop-page">
      {/* Your existing JSX, but now products come from API */}
      <div className="products-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <img src={product.image} alt={product.name} />
            <h3>{product.name}</h3>
            <p className="price">₹{product.price}</p>
            <p className="category">{product.category_name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Shop;
```

### Custom Order Form Example

```javascript
// src/pages/CustomOrder/CustomOrder.js
import React, { useState } from 'react';
import APIService from '../../services/api';
import './CustomOrder.css';

const CustomOrder = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    material: 'PLA',
    color: '',
    description: '',
    budget: '',
    quantity: '1',
  });
  const [file, setFile] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      // Create FormData object for file upload
      const formDataObj = new FormData();
      Object.keys(formData).forEach(key => {
        formDataObj.append(key, formData[key]);
      });
      if (file) {
        formDataObj.append('design_file', file);
      }

      const response = await APIService.submitCustomOrder(formDataObj);
      alert(response.message);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        phone: '',
        material: 'PLA',
        color: '',
        description: '',
        budget: '',
        quantity: '1',
      });
      setFile(null);
    } catch (error) {
      alert('Failed to submit order. Please try again.');
      console.error('Error:', error);
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  return (
    <div className="custom-order-page">
      <form onSubmit={handleSubmit}>
        {/* Your existing form fields */}
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
        {/* ... other fields ... */}
        
        <input
          type="file"
          onChange={handleFileChange}
          accept=".stl,.obj,.3mf,.step,.stp,.jpg,.jpeg,.png,.pdf"
        />
        
        <button type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Order'}
        </button>
      </form>
    </div>
  );
};

export default CustomOrder;
```

### Contact Form Example

```javascript
// src/pages/Contact/Contact.js
import React, { useState } from 'react';
import APIService from '../../services/api';
import './Contact.css';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await APIService.submitContact(formData);
      alert(response.message);
      
      // Reset form
      setFormData({
        name: '',
        email: '',
        subject: '',
        message: ''
      });
    } catch (error) {
      alert('Failed to send message. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="contact-page">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          required
        />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleInputChange}
          required
        />
        <input
          type="text"
          name="subject"
          value={formData.subject}
          onChange={handleInputChange}
          required
        />
        <textarea
          name="message"
          value={formData.message}
          onChange={handleInputChange}
          required
        />
        <button type="submit" disabled={submitting}>
          {submitting ? 'Sending...' : 'Send Message'}
        </button>
      </form>
    </div>
  );
};

export default Contact;
```

### Newsletter Subscription Example

```javascript
// src/components/Layout/Footer.js
import React, { useState } from 'react';
import APIService from '../../services/api';
import './Footer.css';

const Footer = () => {
  const [email, setEmail] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const response = await APIService.subscribeNewsletter(email);
      alert(response.message);
      setEmail('');
    } catch (error) {
      alert('Failed to subscribe. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <footer className="footer">
      <form onSubmit={handleNewsletterSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          required
        />
        <button type="submit" disabled={submitting}>
          {submitting ? 'Subscribing...' : 'Subscribe'}
        </button>
      </form>
    </footer>
  );
};

export default Footer;
```

## 🖼️ Step 5: Handle Media Files

Since the backend serves media files, update image URLs:

```javascript
// Before (placeholder)
<img src="/assets/products/planter.jpg" alt="Product" />

// After (from API)
<img src={product.image} alt={product.name} />
// The API returns full URLs like: http://localhost:8000/media/products/planter.jpg
```

## 🔍 Step 6: Add Loading States

```javascript
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  const loadData = async () => {
    try {
      setLoading(true);
      const data = await APIService.getProducts();
      setProducts(data.results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  loadData();
}, []);

if (loading) return <div>Loading...</div>;
if (error) return <div>Error: {error}</div>;
```

## 🚨 Step 7: Error Handling

Create an error boundary component:

```javascript
// src/components/ErrorBoundary.js
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-page">
          <h1>Oops! Something went wrong.</h1>
          <p>Please try refreshing the page.</p>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

## 🧪 Step 8: Test Integration

1. Start Django backend:
```bash
python manage.py runserver
```

2. Start React frontend:
```bash
npm start
```

3. Test each feature:
   - Browse products
   - View product details
   - Submit custom order (with file upload)
   - Send contact message
   - Subscribe to newsletter

## 🌐 Step 9: Production Deployment

1. Deploy backend to Railway (follow DEPLOYMENT.md)

2. Update React `.env` for production:
```env
REACT_APP_API_URL=https://your-app.railway.app/api
```

3. Build React app:
```bash
npm run build
```

4. Deploy to Vercel/Netlify

## 🔐 Step 10: CORS Configuration

Ensure backend allows your frontend domain:

In backend `.env`:
```env
CORS_ALLOWED_ORIGINS=https://printbox3d.com,https://www.printbox3d.com
```

## ✅ Integration Checklist

- [ ] API service created
- [ ] Environment variables configured
- [ ] Shop page connected to API
- [ ] Product detail page connected
- [ ] Custom order form working
- [ ] Contact form working
- [ ] Newsletter subscription working
- [ ] Image URLs updated
- [ ] Loading states added
- [ ] Error handling implemented
- [ ] CORS configured
- [ ] Production URLs updated
- [ ] Both apps deployed
- [ ] End-to-end testing completed

## 🆘 Common Issues

### CORS Errors
**Problem**: "Access to fetch has been blocked by CORS policy"
**Solution**: Add your frontend URL to `CORS_ALLOWED_ORIGINS` in backend

### 404 Errors
**Problem**: API endpoints return 404
**Solution**: Check API_BASE_URL includes `/api` at the end

### File Upload Fails
**Problem**: File upload returns error
**Solution**: Make sure you're using FormData, not JSON for file uploads

### Images Not Loading
**Problem**: Product images don't display
**Solution**: Check media files are being served correctly, use full URLs from API

## 📚 Additional Resources

- React Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- FormData: https://developer.mozilla.org/en-US/docs/Web/API/FormData
- Error Boundaries: https://reactjs.org/docs/error-boundaries.html

---

**Your frontend is now fully integrated with the Django backend! 🎉**
