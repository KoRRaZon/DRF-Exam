from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.profiles.serializers import ShippingAddressSerializer
from apps.shop.models import Product


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField()

#  используется для сериализации данных о продавце (магазине)
class SellerShopSerializer(serializers.Serializer):
    name = serializers.CharField(source="business_name")
    slug = serializers.SlugField()
    avatar = serializers.CharField(source="user.avatar")


# предназначен для сериализации данных о продукте
class ProductSerializer(serializers.Serializer):
    seller = SellerShopSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    desc = serializers.CharField()
    average_rating = serializers.SerializerMethodField()
    price_old = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = CategorySerializer()
    in_stock = serializers.IntegerField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = [
            "seller", "name", "slug", "desc", "average_rating",
            "price_current", "price", "category",
            "in_stock", "image1", "image2", "image3"
        ]


# похожий на ProductSerializer, но предназначен для создания продукта
class CreateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    desc = serializers.CharField()
    price_current = serializers.DecimalField(max_digits=10, decimal_places=2)
    category_slug = serializers.SlugField()
    in_stock = serializers.IntegerField()
    image1 = serializers.ImageField()
    image2 = serializers.ImageField(required=False)
    image3 = serializers.ImageField(required=False)

# используется для представления информации о продукте внутри элемента заказа (то есть, товара в корзине)
class OrderItemProductSerializer(serializers.Serializer):
    seller = SellerShopSerializer()
    name = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price_current"
    )

# используется для представления всего элемента заказа (то есть, записи в корзине)
class OrderItemSerializer(serializers.Serializer):
    product = OrderItemProductSerializer()
    quantity = serializers.IntegerField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2, source="get_total")


# используется для валидации данных, отправленных клиентом при добавлении, обновлении или удалении товара из корзины
class ToggleCartItemSerializer(serializers.Serializer):
    slug = serializers.SlugField()
    quantity = serializers.IntegerField(min_value=0)

# используется для валидации данных, связанных с этапом оформления заказа до создания самого заказа
class CheckoutSerializer(serializers.Serializer):
    shipping_id = serializers.UUIDField()

# представления данных о заказе после его создания, включает в себя информацию о пользователе, статусе доставки и оплаты, стоимости и других деталях
class OrderSerializer(serializers.Serializer):
    tx_ref = serializers.CharField()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    delivery_status = serializers.CharField()
    payment_status = serializers.CharField()
    date_delivered = serializers.DateTimeField()
    shipping_details = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(
        max_digits=100, decimal_places=2, source="get_cart_subtotal"
    )
    total = serializers.DecimalField(
        max_digits=100, decimal_places=2, source="get_cart_total"
    )

    @extend_schema_field(ShippingAddressSerializer)
    def get_shipping_details(self, obj):
        return ShippingAddressSerializer(obj).data

# сериализатор для представления позиции в заказе
class CheckItemOrderSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    total = serializers.FloatField(source="get_total")


class ReviewSerializer(serializers.Serializer):
    user = serializers.CharField(source="user.full_name")
    product = serializers.CharField(source="product.name")
    rating = serializers.IntegerField()
    text = serializers.CharField()