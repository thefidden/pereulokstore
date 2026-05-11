from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.filters import ProductFilter
from api.models import Product
from api.serializer import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @silk_profile(name = 'Product List')
    def list(self, request: Request) -> Response:
        products = Product.objects.all().optimized()
        filterset = ProductFilter(request.query_params, queryset = products)

        if not filterset.is_valid():
            return Response(filterset.errors, status = status.HTTP_400_BAD_REQUEST)

        products_filtered = filterset.qs
        serializer = ProductSerializer(products_filtered, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Retrieve')
    def retrieve(self, request: Request, pk) -> Response:
        product = get_object_or_404(Product, id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Create')
    def create(self, request: Request) -> Response:
        # Проверка прав администратора
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response(status = status.HTTP_403_FORBIDDEN)

        serializer = ProductSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    @silk_profile(name = 'Product Delete')
    def delete(self, request: Request, pk) -> Response:
        product = get_object_or_404(Product, id = pk)
        product.delete()
        return Response(
            f"Product {product.id} was deleted from database",
            status = status.HTTP_204_NO_CONTENT
        )

    @silk_profile(name = 'Product Update')
    def partial_update(self, request: Request, pk) -> Response:
        # Поля для обновления
        name = request.data.get('name')
        new_type = request.data.get('type')
        price = request.data.get('price')
        description = request.data.get('description')

        data: dict[str, str] = dict()

        if name is not None: data['name'] = name
        if new_type is not None: data['type'] = new_type
        if price is not None: data['price'] = price
        if description is not None: data['description'] = description

        product: Product = get_object_or_404(Product, id = pk)
        serializer = ProductSerializer(product, data = data, partial = True)
        serializer.is_valid()
        return Response(data = serializer.data, status = status.HTTP_200_OK)
