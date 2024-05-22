from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem
from .serializers import OrderItemSerializer, UpdateOrderItemSerializer
import requests
import json
from django.views.decorators.csrf import csrf_exempt

class OrderItemListView(APIView):
    def get(self, request):
        order_items = OrderItem.objects.all()  # is_active không có trong model OrderItem
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListByStatus(APIView):
    def get(self, request):
        status_param = request.query_params.get('status')  # Dùng query_params thay cho request.data
        order_items = OrderItem.objects.filter(status=status_param)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToOrderView(APIView):
    @csrf_exempt
    def post(self, request):
        token_verification_url = "http://127.0.0.1:4000/api/ecomSys/user/verify-token/"
        headers = {'Authorization': request.headers.get('Authorization')}
        response = requests.get(token_verification_url, headers=headers)
        if response.status_code == 200:
            user_id = request.data.get('user_id')
            product_id = request.data.get('product_id')
            created_at = request.data.get('created_at')
            order_item = OrderItem.objects.filter(product_id=product_id, user_id=user_id, created_at=created_at).first()
            if order_item:
                serializer = UpdateOrderItemSerializer(instance=order_item, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = OrderItemSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

class OrderItemView(APIView):
    def get(self, request):
        token_verification_url = "http://127.0.0.1:4000/api/ecomSys/user/verify-token/"
        headers = {'Authorization': request.headers.get('Authorization')}
        response = requests.get(token_verification_url, headers=headers)
        if response.status_code == 200:
            user_id = response.data.get('user_id')
            order_id = request.query_params.get('order_id')  # Chuyển sang dùng query_params cho order_id
            created_at = request.query_params.get('created_at')  # Chuyển sang dùng query_params cho created_at
            order_item = OrderItem.objects.filter(user_id=user_id, order_item_id=order_id, created_at=created_at).first()
            if not order_item:
                return Response({'error': 'Order item not found.'}, status=status.HTTP_404_NOT_FOUND)

            order_total = 0
            product = self.get_product(order_item.type, order_item.product_id)
            shipment = self.get_shipment(order_item.shipment_id)
            if product:
                order_total = order_item.quantity * product.get('price', 0) * (100 - product.get('sale', 0)) / 100

            if shipment:
                order_total += shipment.get('price', 0)

            response_data = {
                'order_item': OrderItemSerializer(order_item).data,
                'total': order_total
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_product(self, type, product_id):
        if type == 'book':
            product_url = "http://localhost:4002/api/book/detail/{}/".format(product_id)
        elif type == 'mobile':
            product_url = "http://localhost:4002/api/mobile/detail/{}/".format(product_id)
        elif type == 'clothes':
            product_url = "http://localhost:4002/api/clothes/detail/{}/".format(product_id)
        else:
            return None

        response = requests.get(product_url)
        if response.status_code == 200:
            return response.json()
        return None

    def get_shipment(self, shipment_id):
        shipment_url = "http://localhost:4002/api/shipment/detail/{}/".format(shipment_id)
        response = requests.get(shipment_url)
        if response.status_code == 200:
            return response.json()
        return None
