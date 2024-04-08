from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()
router.register(r'alerts', GenreViewSet, basename='alerts')

urlpatterns = [
    path('', BookListCreateAPIView.as_view(), name='index'),
    path('<int:pk>/<str:price>', BookDetailAPIView.as_view(), name='book-detail'),
    path('login', Login.as_view(), name='login'),
    path('register', register.as_view(), name='register'),
    path('alert/', include(router.urls)),
    path('token/pair/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]