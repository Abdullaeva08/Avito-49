from rest_framework import viewsets, generics, status, serializers, permissions
from rest_framework.filters import SearchFilter
from .serializers import FavoriteSerializer
from .serializers import (UserProfileListSerializer, UserProfileListSerializer, CategoryListSerializer,
                          SubCategoryListSerializer, ProductListSerializer,
                          ReviewSerializer, ProductDetailSerializer, CategoryDetailSerializer,
                          SubCategoryDetailSerializer, RegisterSerializer, CustomLoginSerializer, LogoutSerializer,
                          CartSerializer, CartItemSerializer, FavoriteItem, FavoriteItemSerializer)
from django.contrib.auth.models import AnonymousUser
from .models import UserProfile, Product, Category, SubCategory,  CartItem, Cart, FavoriteItem, Favorite, Review
from .filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductPagination

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken()
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user)



class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class =SubCategoryListSerializer

class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategoryDetailSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'created_date']
    pagination_class = ProductPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return CartItem.objects.none()

        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class FavoriteAPIView(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class =  FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return FavoriteItem.objects.none()

        return FavoriteItem.objects.filter(favorite__user=self.request.user)


    def perform_create(self, serializer):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']

        if FavoriteItem.objects.filter(favorite=favorite, product=product).exists():
            raise serializers.ValidationError('Товар кошулган')

        serializer.save(favorite=favorite)


