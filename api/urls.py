from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CategoryViewSet, MaterialViewSet, ProductViewSet,
    CustomOrderViewSet, ContactMessageViewSet,
    NewsletterViewSet, TestimonialViewSet,
    create_order, verify_payment_simple, get_order_status, payment_failed,
    get_user_orders, get_s3_upload_url, razorpay_webhook,
)
from .auth_views import register, login, logout, get_user_profile, update_user_profile

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'custom-orders', CustomOrderViewSet, basename='custom-order')
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')

urlpatterns = [
    path('', include(router.urls)),

    # Authentication endpoints
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', get_user_profile, name='profile'),
    path('auth/profile/update/', update_user_profile, name='profile_update'),

    # Payment endpoints
    path('orders/create/', create_order, name='create_order'),
    path('orders/verify-payment/', csrf_exempt(verify_payment_simple), name='verify_payment'),
    path('orders/payment-failed/', payment_failed, name='payment_failed'),
    path('orders/user/me/', get_user_orders, name='user_orders'),
    path('orders/<str:order_id>/', get_order_status, name='order_status'),

    # Razorpay webhook (CSRF exempt — signature verified internally)
    path('payments/webhook/', razorpay_webhook, name='razorpay_webhook'),

    # S3 presigned upload
    path('s3/presigned-upload/', get_s3_upload_url, name='s3_presigned_upload'),
]
