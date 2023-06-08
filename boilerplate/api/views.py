from django.contrib.auth.models import User, Group
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets
from api.models import Product
from api.serializers import ProductSerializer
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # Allow unauthenticated access for safe methods (GET, HEAD, OPTIONS)
            return True
        return request.user and request.user.is_authenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # UNAUTHICATED USER -> READ ONLY
    # AUTHENTICATED USER -> ALL
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # RATE LIMITER ( LIMIT RATE IS AT SETTINGS.PY )
    throttle_classes = [UserRateThrottle]
