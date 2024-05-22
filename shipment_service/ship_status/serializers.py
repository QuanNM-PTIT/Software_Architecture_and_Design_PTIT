from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

    def create(self, validated_data):
        shipment_type = validated_data.get('shipment_type')
        validated_data['price'] = self.calculate_price(shipment_type)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'shipment_type' in validated_data:
            shipment_type = validated_data.get('shipment_type')
            instance.price = self.calculate_price(shipment_type)
        instance.username = validated_data.get('username', instance.username)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.shipment_status = validated_data.get('shipment_status', instance.shipment_status)
        instance.shipment_type = validated_data.get('shipment_type', instance.shipment_type)
        instance.save()
        return instance

    def calculate_price(self, shipment_type):
        if shipment_type == 'hoả tốc':
            return 50
        elif shipment_type == 'nhanh':
            return 20
        elif shipment_type == 'tiết kiệm':
            return 10
        return 0
