"""ViewSet для управления товарами."""

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from silk.profiling.profiler import silk_profile

from api.filters import ProductFilter
from api.models.Product import Product
from api.serializers.ProductSerializer import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    """ViewSet для управления товарами.
    
    Обеспечивает CRUD операции для товаров с поддержкой фильтрации
    и профилированием через Django Silk.
    """
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    @silk_profile(name = 'Product List')
    def list(self, request: Request) -> Response:
        """Получает список товаров с поддержкой фильтрации.
        
        Args:
            request: HTTP запрос с параметрами фильтрации.
            
        Returns:
            Response: Список товаров или ошибки валидации фильтров.
        """
        products = Product.objects.all().optimized()
        filterset = ProductFilter(request.query_params, queryset = products)

        if not filterset.is_valid():
            return Response(filterset.errors, status = status.HTTP_400_BAD_REQUEST)

        products_filtered = filterset.qs
        serializer = ProductSerializer(products_filtered, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Retrieve')
    def retrieve(self, request: Request, pk) -> Response:
        """Получает детальную информацию о товаре.
        
        Args:
            request: HTTP запрос.
            pk: ID товара.
            
        Returns:
            Response: Данные товара или 404 если не найден.
        """
        product = get_object_or_404(Product, id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status = status.HTTP_200_OK)

    @silk_profile(name = 'Product Create')
    def create(self, request: Request) -> Response:
        """Создает новый товар (только для администраторов).
        
        Args:
            request: HTTP запрос с данными товара.
            
        Returns:
            Response: Созданный товар, ошибки валидации или 403.
        """
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
        """Удаляет товар.
        
        Args:
            request: HTTP запрос.
            pk: ID товара.
            
        Returns:
            Response: 204 при успешном удалении или 404.
        """
        product = get_object_or_404(Product, id = pk)
        product.delete()
        return Response(
            f"Product {product.id} was deleted from database",
            status = status.HTTP_204_NO_CONTENT
        )

    @silk_profile(name = 'Product Update')
    def partial_update(self, request: Request, pk) -> Response:
        """Частично обновляет товар.
        
        Args:
            request: HTTP запрос с полями для обновления.
            pk: ID товара.
            
        Returns:
            Response: Обновленные данные товара или 404.
        """
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
