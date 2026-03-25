from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from .serializers import orderSerializer, orderItemSerializer
from .models import order
from rest_framework.response import Response

# Create your views here.

class orderView(viewsets.ModelViewSet):
    serializer_class = orderSerializer

    def create(self, request, *args, **kwargs):
        from django.contrib.auth.models import User
        from .models import orderItem

        user = request.user
        existing_order = order.objects.filter(user=user, ordered=False).first()
        if existing_order:
            # 如果存在未完成的訂單，將新的訂單項目添加到現有的訂單中
            order_item = orderItem.objects.create(
                order = existing_order, 
                game_id = request.data['game_id']
                )
            serializer = orderItemSerializer(order_item)
            return Response(serializer.data)
        else:
            # 如果不存在未完成的訂單，則創建新的訂單，並添加訂單
            new_order = order.objects.create(user=user)
            order_item = orderItem.objects.create(
                order = new_order,
                game_id = request.data['game_id']
            )
            serializer = orderItemSerializer(order_item)
            return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        from django.contrib.auth.models import User
        from .models import orderItem
        try:
            user = request.user
            existing_order = order.objects.filter(user=user, ordered=False).first()
            order_item_instance = orderItem.objects.get(
                order = existing_order,
                id = self.kwargs['pk']
            )
            order_item_instance.delete()
            return Response({'success': 'orderItem:' + self.kwargs['pk'] + 'deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        user = self.request.user
        queryset = order.objects.filter(user=user, ordered=False)
        return queryset
    
    def get_order_count(self, request, *args, **kwargs):
        orders = order.objects.filter(user=self.request.user, ordered=False)
        order_count = sum(len(order.games.all()) for order in orders)
        return Response({'order_count': order_count})