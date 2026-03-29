from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .serializers import orderSerializer, orderItemSerializer
from .models import order, orderItem
from gameprofile.models import profile
from rest_framework.response import Response

# Create your views here.

class orderView(viewsets.ModelViewSet):
    serializer_class = orderSerializer
    # 確保是認證用戶才能訪問購物車功能
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            game_id = request.data.get('game_id')
            
            # 驗證 game_id
            if not game_id:
                return Response(
                    {'error': 'game_id is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 檢查遊戲是否存在
            try:
                profile.objects.get(id=game_id)
            except profile.DoesNotExist:
                return Response(
                    {'error': f'Game with id {game_id} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # 查找或創建未完成訂單
            existing_order = order.objects.filter(user=user, ordered=False).first()
            if existing_order:
                order_obj = existing_order
            else:
                order_obj = order.objects.create(user=user)
            
            # 創建訂單項目
            order_item = orderItem.objects.create(
                order=order_obj,
                game_id=game_id
            )
            
            serializer = orderItemSerializer(order_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            user = request.user
            existing_order = order.objects.filter(user=user, ordered=False).first()
            
            if not existing_order:
                return Response(
                    {'error': 'No active order found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            try:
                order_item_instance = orderItem.objects.get(
                    order=existing_order,
                    id=self.kwargs['pk']
                )
            except orderItem.DoesNotExist:
                return Response(
                    {'error': f'Order item with id {self.kwargs["pk"]} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            order_item_instance.delete()
            return Response(
                {'success': f'Order item {self.kwargs["pk"]} deleted successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except orderItem.DoesNotExist:
            return Response(
                {'error': 'Order item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_queryset(self):
        user = self.request.user
        return order.objects.filter(user=user, ordered=False)
    
    @action(detail=False, methods=['get'])
    def cart_count(self, request, *args, **kwargs):
        """獲取購物車中的商品總數（未完成訂單中的項目數）"""
        try:
            # 獲取所有未完成的訂單（購物車）
            pending_orders = order.objects.filter(user=self.request.user, ordered=False)
            # 計算所有購物車中的商品總數
            total_items = sum(order_obj.order_items.count() for order_obj in pending_orders)
            return Response({
                'cart_count': total_items,
                'pending_orders': pending_orders.count()
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )