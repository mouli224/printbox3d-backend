# Razorpay Payment Integration Guide

Complete guide for integrating Razorpay payment gateway in PrintBox3D application.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Backend Setup](#backend-setup)
3. [Frontend Integration](#frontend-integration)
4. [API Endpoints](#api-endpoints)
5. [Payment Flow](#payment-flow)
6. [Testing](#testing)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

Razorpay is integrated into PrintBox3D to handle:
- ✅ Product purchases from the shop
- ✅ Secure payment processing
- ✅ Order tracking and management
- ✅ Payment verification and signature validation
- ✅ Inventory management (automatic stock reduction)

### Features
- **Order Creation**: Create orders with multiple items from cart
- **Payment Processing**: Secure payment through Razorpay
- **Payment Verification**: Server-side signature verification
- **Order Tracking**: Track order and payment status
- **Stock Management**: Automatic stock updates on successful payment

---

## 🔧 Backend Setup

### 1. Install Dependencies

The required package is already added to `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Get Razorpay API Keys

**Test Mode (Development):**
1. Sign up at [razorpay.com](https://razorpay.com)
2. Go to Settings → API Keys → Test Mode
3. Generate test keys

**Live Mode (Production):**
1. Complete KYC verification
2. Go to Settings → API Keys → Live Mode
3. Generate live keys

### 3. Configure Environment Variables

Add to Railway environment variables:

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

**Local Development (.env):**
```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

### 4. Run Migrations

Create database tables for orders and payments:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Verify Setup

Test in Django shell:

```python
python manage.py shell

from django.conf import settings
print(f"Razorpay Key ID: {settings.RAZORPAY_KEY_ID}")
print(f"Razorpay Secret: {'✓ Set' if settings.RAZORPAY_KEY_SECRET else '✗ Not Set'}")
```

---

## 🌐 Frontend Integration

### 1. Add Razorpay Checkout Script

Add to your frontend `public/index.html`:

```html
<head>
  <!-- Other head content -->
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
```

### 2. Create Checkout Component

Create `src/pages/Checkout/Checkout.js`:

```jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import './Checkout.css';

const Checkout = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_email: '',
    customer_phone: '',
    shipping_address: '',
    shipping_city: '',
    shipping_state: '',
    shipping_pincode: ''
  });

  // Get cart items from CartContext or localStorage
  const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const loadRazorpayScript = () => {
    return new Promise((resolve) => {
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => resolve(true);
      script.onerror = () => resolve(false);
      document.body.appendChild(script);
    });
  };

  const handlePayment = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Load Razorpay script
      const scriptLoaded = await loadRazorpayScript();
      if (!scriptLoaded) {
        alert('Failed to load payment gateway. Please try again.');
        setLoading(false);
        return;
      }

      // Create order
      const orderData = {
        ...formData,
        items: cartItems.map(item => ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      const response = await api.post('/orders/create/', orderData);
      const {
        order_id,
        razorpay_order_id,
        razorpay_key_id,
        amount,
        currency,
        customer_name,
        customer_email,
        customer_phone
      } = response.data;

      // Razorpay options
      const options = {
        key: razorpay_key_id,
        amount: amount,
        currency: currency,
        name: 'PrintBox3D',
        description: `Order #${order_id}`,
        order_id: razorpay_order_id,
        handler: async (response) => {
          try {
            // Verify payment
            const verifyResponse = await api.post('/orders/verify-payment/', {
              razorpay_order_id: response.razorpay_order_id,
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_signature: response.razorpay_signature,
              order_id: order_id
            });

            // Clear cart
            localStorage.removeItem('cart');

            // Redirect to success page
            navigate(`/order-success/${order_id}`);
          } catch (error) {
            console.error('Payment verification failed:', error);
            alert('Payment verification failed. Please contact support.');
          }
        },
        prefill: {
          name: customer_name,
          email: customer_email,
          contact: customer_phone
        },
        theme: {
          color: '#3399cc'
        },
        modal: {
          ondismiss: async () => {
            // Payment cancelled
            await api.post('/orders/payment-failed/', {
              order_id: order_id,
              error_description: 'Payment cancelled by user'
            });
            alert('Payment cancelled');
            setLoading(false);
          }
        }
      };

      const razorpay = new window.Razorpay(options);
      razorpay.on('payment.failed', async (response) => {
        // Payment failed
        await api.post('/orders/payment-failed/', {
          order_id: order_id,
          error_description: response.error.description
        });
        alert(`Payment failed: ${response.error.description}`);
        setLoading(false);
      });

      razorpay.open();
    } catch (error) {
      console.error('Error creating order:', error);
      alert(error.response?.data?.error || 'Failed to create order');
      setLoading(false);
    }
  };

  return (
    <div className="checkout-container">
      <h1>Checkout</h1>
      <form onSubmit={handlePayment}>
        <h2>Customer Details</h2>
        <input
          type="text"
          name="customer_name"
          placeholder="Full Name"
          value={formData.customer_name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="customer_email"
          placeholder="Email"
          value={formData.customer_email}
          onChange={handleChange}
          required
        />
        <input
          type="tel"
          name="customer_phone"
          placeholder="Phone Number"
          value={formData.customer_phone}
          onChange={handleChange}
          required
        />

        <h2>Shipping Address</h2>
        <textarea
          name="shipping_address"
          placeholder="Street Address"
          value={formData.shipping_address}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="shipping_city"
          placeholder="City"
          value={formData.shipping_city}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="shipping_state"
          placeholder="State"
          value={formData.shipping_state}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="shipping_pincode"
          placeholder="Pincode"
          value={formData.shipping_pincode}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Proceed to Payment'}
        </button>
      </form>
    </div>
  );
};

export default Checkout;
```

### 3. Create Order Success Page

Create `src/pages/OrderSuccess/OrderSuccess.js`:

```jsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../../services/api';
import './OrderSuccess.css';

const OrderSuccess = () => {
  const { orderId } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOrder = async () => {
      try {
        const response = await api.get(`/orders/${orderId}/`);
        setOrder(response.data);
      } catch (error) {
        console.error('Error fetching order:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrder();
  }, [orderId]);

  if (loading) return <div>Loading...</div>;
  if (!order) return <div>Order not found</div>;

  return (
    <div className="order-success">
      <div className="success-icon">✓</div>
      <h1>Payment Successful!</h1>
      <p>Thank you for your order</p>
      
      <div className="order-details">
        <h2>Order Details</h2>
        <p><strong>Order ID:</strong> {order.order_id}</p>
        <p><strong>Total Amount:</strong> ₹{order.total_amount}</p>
        <p><strong>Status:</strong> {order.status}</p>
        
        <h3>Items:</h3>
        {order.items.map(item => (
          <div key={item.id} className="order-item">
            <p>{item.product_name} x {item.quantity}</p>
            <p>₹{item.subtotal}</p>
          </div>
        ))}
        
        <h3>Shipping Address:</h3>
        <p>{order.shipping_address}</p>
        <p>{order.shipping_city}, {order.shipping_state} - {order.shipping_pincode}</p>
      </div>
    </div>
  );
};

export default OrderSuccess;
```

### 4. Update Routes

Add to `src/App.js`:

```jsx
import Checkout from './pages/Checkout/Checkout';
import OrderSuccess from './pages/OrderSuccess/OrderSuccess';

function App() {
  return (
    <Routes>
      {/* Existing routes */}
      <Route path="/checkout" element={<Checkout />} />
      <Route path="/order-success/:orderId" element={<OrderSuccess />} />
    </Routes>
  );
}
```

---

## 🔌 API Endpoints

### 1. Create Order

**POST** `/api/orders/create/`

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "9876543210",
  "shipping_address": "123 Main St",
  "shipping_city": "Mumbai",
  "shipping_state": "Maharashtra",
  "shipping_pincode": "400001",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

**Response (201 Created):**
```json
{
  "order_id": "ORD20241124123456ABCD",
  "razorpay_order_id": "order_xxxxxxxxxxxxxx",
  "razorpay_key_id": "rzp_test_xxxxxxxxxxxxxx",
  "amount": 299800,
  "currency": "INR",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "9876543210"
}
```

### 2. Verify Payment

**POST** `/api/orders/verify-payment/`

**Request Body:**
```json
{
  "razorpay_order_id": "order_xxxxxxxxxxxxxx",
  "razorpay_payment_id": "pay_xxxxxxxxxxxxxx",
  "razorpay_signature": "signature_string",
  "order_id": "ORD20241124123456ABCD"
}
```

**Response (200 OK):**
```json
{
  "message": "Payment verified successfully",
  "order_id": "ORD20241124123456ABCD",
  "status": "PAID"
}
```

### 3. Get Order Status

**GET** `/api/orders/{order_id}/`

**Response (200 OK):**
```json
{
  "id": 1,
  "order_id": "ORD20241124123456ABCD",
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "customer_phone": "9876543210",
  "shipping_address": "123 Main St",
  "shipping_city": "Mumbai",
  "shipping_state": "Maharashtra",
  "shipping_pincode": "400001",
  "status": "PAID",
  "total_amount": "2998.00",
  "payment_status": "CAPTURED",
  "tracking_number": "",
  "items": [
    {
      "id": 1,
      "product_name": "3D Printed Vase",
      "product_price": "999.00",
      "product_image": "https://example.com/media/products/vase.jpg",
      "quantity": 2,
      "subtotal": "1998.00"
    }
  ],
  "created_at": "2024-11-24T12:34:56.789Z",
  "updated_at": "2024-11-24T12:35:30.123Z"
}
```

### 4. Payment Failed

**POST** `/api/orders/payment-failed/`

**Request Body:**
```json
{
  "order_id": "ORD20241124123456ABCD",
  "error_description": "Payment cancelled by user"
}
```

---

## 🔄 Payment Flow

```
1. User adds items to cart
   ↓
2. User goes to checkout page
   ↓
3. User fills shipping details
   ↓
4. Frontend calls /api/orders/create/
   ↓
5. Backend creates Order and Razorpay order
   ↓
6. Backend returns Razorpay order details
   ↓
7. Frontend opens Razorpay checkout modal
   ↓
8. User completes payment
   ↓
9. Razorpay returns payment details
   ↓
10. Frontend calls /api/orders/verify-payment/
   ↓
11. Backend verifies signature
   ↓
12. Backend updates order status to PAID
   ↓
13. Backend reduces product stock
   ↓
14. Frontend redirects to success page
```

---

## 🧪 Testing

### Test Mode Cards

Use these test cards in test mode:

**Successful Payment:**
- Card Number: `4111 1111 1111 1111`
- CVV: Any 3 digits
- Expiry: Any future date

**Failed Payment:**
- Card Number: `4111 1111 1111 1112`
- CVV: Any 3 digits
- Expiry: Any future date

### Testing Checklist

- [ ] Create order with single item
- [ ] Create order with multiple items
- [ ] Test successful payment
- [ ] Test payment failure
- [ ] Test payment cancellation
- [ ] Verify stock reduction after payment
- [ ] Check order status page
- [ ] Test with out-of-stock product
- [ ] Verify signature validation

---

## 🚀 Production Deployment

### 1. Switch to Live Mode

Replace test keys with live keys in Railway:

```env
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
```

### 2. Webhook Setup (Optional)

Configure webhooks in Razorpay dashboard for:
- Payment captured
- Payment failed
- Refund processed

**Webhook URL:**
```
https://your-backend.railway.app/api/webhooks/razorpay/
```

### 3. Security Checklist

- [ ] Live keys configured in Railway
- [ ] Test keys removed from production
- [ ] HTTPS enabled on frontend and backend
- [ ] CORS properly configured
- [ ] Signature verification working
- [ ] Error handling in place

---

## 🛠️ Troubleshooting

### Payment Modal Not Opening

**Check:**
1. Razorpay script loaded: `window.Razorpay`
2. Valid `razorpay_key_id` in response
3. Browser console for errors

### Payment Verification Failing

**Check:**
1. `RAZORPAY_KEY_SECRET` set in backend
2. Signature calculation correct
3. Order ID matches

### Stock Not Reducing

**Check:**
1. Payment verification successful
2. Order status changed to PAID
3. Product stock_quantity field

### Order Creation Error

**Check:**
1. All required fields provided
2. Product IDs valid
3. Product stock available
4. Database connection working

---

## 📚 Additional Resources

- [Razorpay Documentation](https://razorpay.com/docs/)
- [Razorpay Integration Guide](https://razorpay.com/docs/payments/payment-gateway/web-integration/)
- [Django Razorpay](https://github.com/razorpay/razorpay-python)

---

**Integration Complete!** 🎉

Your PrintBox3D application now supports secure online payments through Razorpay.
