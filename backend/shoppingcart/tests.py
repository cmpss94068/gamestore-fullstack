from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from decimal import Decimal
from gameprofile.models import profile, platform, category
from .models import order, orderItem
from datetime import date


class OrderModelTest(TestCase):
    """訂單模型測試"""

    def setUp(self):
        """測試前的準備"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.platform = platform.objects.create(name="PC")
        self.category = category.objects.create(name="RPG")
        
        self.game1 = profile.objects.create(
            game_name="Game 1",
            game_img="https://example.com/g1.jpg",
            game_url="https://store.example.com/game1",
            game_rating=Decimal("8.0"),
            game_price=Decimal("50"),
            game_date=date.today(),
            game_publisher="Publisher 1"
        )
        self.game1.platform.add(self.platform)
        self.game1.category.add(self.category)

    def test_create_order_successfully(self):
        """測試成功創建訂單"""
        order_obj = order.objects.create(user=self.user, ordered=False)
        self.assertEqual(order_obj.user, self.user)
        self.assertFalse(order_obj.ordered)
        self.assertEqual(str(order_obj), f"Order {order_obj.pk}")

    def test_get_total_price_empty_order(self):
        """測試空訂單的總金額"""
        order_obj = order.objects.create(user=self.user, ordered=False)
        self.assertEqual(order_obj.get_total_price(), 0)

    def test_get_total_price_with_items(self):
        """測試包含商品的訂單總金額"""
        order_obj = order.objects.create(user=self.user, ordered=False)
        
        item1 = orderItem.objects.create(
            order=order_obj,
            game=self.game1,
            quantity=2
        )
        
        game2 = profile.objects.create(
            game_name="Game 2",
            game_img="https://example.com/g2.jpg",
            game_url="https://store.example.com/game2",
            game_rating=Decimal("7.5"),
            game_price=Decimal("30"),
            game_date=date.today(),
            game_publisher="Publisher 2"
        )
        game2.platform.add(self.platform)
        game2.category.add(self.category)
        
        item2 = orderItem.objects.create(
            order=order_obj,
            game=game2,
            quantity=1
        )
        
        expected_total = (2 * Decimal("50")) + (1 * Decimal("30"))
        self.assertEqual(order_obj.get_total_price(), expected_total)


class OrderItemModelTest(TestCase):
    """訂單項目模型測試"""

    def setUp(self):
        """測試前的準備"""
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.platform = platform.objects.create(name="Xbox")
        self.category = category.objects.create(name="FPS")
        
        self.game = profile.objects.create(
            game_name="FPS Game",
            game_img="https://example.com/fps.jpg",
            game_url="https://store.example.com/fps",
            game_rating=Decimal("9.0"),
            game_price=Decimal("60"),
            game_date=date.today(),
            game_publisher="AAA Studios"
        )
        self.game.platform.add(self.platform)
        self.game.category.add(self.category)
        
        self.order = order.objects.create(user=self.user, ordered=False)

    def test_create_order_item_successfully(self):
        """測試成功創建訂單項目"""
        item = orderItem.objects.create(
            order=self.order,
            game=self.game,
            quantity=1
        )
        self.assertEqual(item.order, self.order)
        self.assertEqual(item.game, self.game)
        self.assertEqual(item.quantity, 1)

    def test_order_item_string_representation(self):
        """測試訂單項目字符串表示"""
        item = orderItem.objects.create(
            order=self.order,
            game=self.game,
            quantity=2
        )
        self.assertEqual(str(item), "2 x FPS Game")

    def test_get_item_price(self):
        """測試計算訂單項目價格"""
        item = orderItem.objects.create(
            order=self.order,
            game=self.game,
            quantity=3
        )
        expected_price = 3 * Decimal("60")
        self.assertEqual(item.get_item_price(), expected_price)


class OrderAPITest(APITestCase):
    """訂單 API 端點測試"""

    def setUp(self):
        """測試前的準備"""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        
        self.platform = platform.objects.create(name="Switch")
        self.category = category.objects.create(name="Adventure")
        
        self.game = profile.objects.create(
            game_name="Adventure Game",
            game_img="https://example.com/adventure.jpg",
            game_url="https://store.example.com/adventure",
            game_rating=Decimal("8.5"),
            game_price=Decimal("40"),
            game_date=date.today(),
            game_publisher="Indie Studio"
        )
        self.game.platform.add(self.platform)
        self.game.category.add(self.category)

    def test_create_first_order(self):
        """測試創建第一個訂單"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post(
            '/api/shoppingcart/order/',
            data={'game_id': self.game.id},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.objects.filter(user=self.user, ordered=False).exists())

    def test_add_item_to_existing_order(self):
        """測試新商品添加到現有訂單"""
        self.client.force_authenticate(user=self.user)
        
        # 創建第一個訂單
        response1 = self.client.post(
            '/api/shoppingcart/order/',
            data={'game_id': self.game.id},
            format='json'
        )
        
        # 創建第二個遊戲
        game2 = profile.objects.create(
            game_name="Another Adventure",
            game_img="https://example.com/adv2.jpg",
            game_url="https://store.example.com/adventure2",
            game_rating=Decimal("8.0"),
            game_price=Decimal("35"),
            game_date=date.today(),
            game_publisher="Studio 2"
        )
        game2.platform.add(self.platform)
        game2.category.add(self.category)
        
        # 添加到現有訂單
        response2 = self.client.post(
            '/api/shoppingcart/order/',
            data={'game_id': game2.id},
            format='json'
        )
        
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # 確認只有一個未完成的訂單
        existing_order = order.objects.filter(user=self.user, ordered=False).first()
        self.assertEqual(existing_order.order_items.count(), 2)

    def test_delete_order_item(self):
        """測試刪除訂單項目"""
        self.client.force_authenticate(user=self.user)
        
        # 創建訂單
        order_obj = order.objects.create(user=self.user, ordered=False)
        item = orderItem.objects.create(
            order=order_obj,
            game=self.game,
            quantity=1
        )
        
        # 刪除項目
        response = self.client.delete(f'/api/shoppingcart/order/{item.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(orderItem.objects.filter(id=item.id).exists())

    def test_get_user_orders(self):
        """測試獲取用戶訂單"""
        self.client.force_authenticate(user=self.user)
        
        # 創建訂單
        order_obj = order.objects.create(user=self.user, ordered=False)
        orderItem.objects.create(
            order=order_obj,
            game=self.game,
            quantity=1
        )
        
        response = self.client.get('/api/shoppingcart/order/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authentication_required(self):
        """測試未認證用戶無法訪問 API"""
        response = self.client.get('/api/shoppingcart/order/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cart_count(self):
        """測試獲取購物車商品總數"""
        self.client.force_authenticate(user=self.user)
        
        # 創建第一個訂單項目
        self.client.post(
            '/api/shoppingcart/order/',
            data={'game_id': self.game.id},
            format='json'
        )
        
        # 創建第二個遊戲並添加到購物車
        game2 = profile.objects.create(
            game_name="Another Game",
            game_img="https://example.com/g2.jpg",
            game_url="https://store.example.com/g2",
            game_rating=Decimal("8.0"),
            game_price=Decimal("50"),
            game_date=date.today(),
            game_publisher="Publisher 2"
        )
        game2.platform.add(self.platform)
        game2.category.add(self.category)
        
        self.client.post(
            '/api/shoppingcart/order/',
            data={'game_id': game2.id},
            format='json'
        )
        
        # 測試 cart_count 端點
        response = self.client.get('/api/shoppingcart/order_count/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cart_count'], 2)  # 兩個商品
        self.assertEqual(response.data['pending_orders'], 1)  # 一個未完成訂單
