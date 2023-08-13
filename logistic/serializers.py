from rest_framework import serializers
from logistic.models import Product, StockProduct, Stock

class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

# class StockProductSerializer(serializers.ModelSerializer):
class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']



class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions', [])
        # создаем склад по его параметрам
        stock = super().create(validated_data)
        for pos in positions:
            StockProduct.objects.create(product=pos['product'], quantity=pos['quantity'], price=pos['price'],
                                        stock=stock)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions', [])
        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for pos in positions:
            defaults = {'quantity':pos['quantity'], 'price':pos['price']}
            StockProduct.objects.update_or_create(product=pos['product'], stock=stock, defaults=defaults)
            # defaults должен передаваться в виде словаря, а не кортежа
        return stock
