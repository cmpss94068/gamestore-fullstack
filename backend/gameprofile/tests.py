from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import date
from .models import profile, platform, category
from .serializers import profilePostSerializer, platformSerializer, categorySerializer


class PlatformModelTest(TestCase):
    """平台模型測試"""

    def test_create_platform_successfully(self):
        """測試成功創建平台"""
        platform_obj = platform.objects.create(name="PlayStation 5")
        self.assertEqual(platform_obj.name, "PlayStation 5")
        self.assertEqual(str(platform_obj), "PlayStation 5")

    def test_unique_platform_name(self):
        """測試平台名稱唯一性"""
        platform.objects.create(name="Xbox Series X")
        with self.assertRaises(Exception):
            platform.objects.create(name="Xbox Series X")


class CategoryModelTest(TestCase):
    """分類模型測試"""

    def test_create_category_successfully(self):
        """測試成功創建分類"""
        category_obj = category.objects.create(name="Action")
        self.assertEqual(category_obj.name, "Action")
        self.assertEqual(str(category_obj), "Action")

    def test_unique_category_name(self):
        """測試分類名稱唯一性"""
        category.objects.create(name="RPG")
        with self.assertRaises(Exception):
            category.objects.create(name="RPG")


class ProfileModelTest(TestCase):
    """遊戲資料模型測試"""

    def setUp(self):
        """測試前的準備"""
        self.platform = platform.objects.create(name="Nintendo Switch")
        self.category = category.objects.create(name="Adventure")

    def test_create_profile_successfully(self):
        """測試成功創建遊戲資料"""
        game = profile.objects.create(
            game_name="Zelda Breath of the Wild",
            game_img="https://example.com/zelda.jpg",
            game_url="https://store.nintendo.com/zelda",
            game_rating=Decimal("9.5"),
            game_price=Decimal("60"),
            game_date=date(2023, 3, 15),
            game_publisher="Nintendo"
        )
        game.platform.add(self.platform)
        game.category.add(self.category)

        self.assertEqual(game.game_name, "Zelda Breath of the Wild")
        self.assertEqual(game.game_price, Decimal("60"))
        self.assertEqual(game.game_publisher, "Nintendo")
        self.assertEqual(str(game), "Zelda Breath of the Wild")

    def test_game_url_unique(self):
        """測試遊戲 URL 唯一性"""
        profile.objects.create(
            game_name="Game 1",
            game_img="https://example.com/g1.jpg",
            game_url="https://unique-url.com/game",
            game_rating=Decimal("8.0"),
            game_price=Decimal("50"),
            game_date=date.today(),
            game_publisher="Publisher"
        )
        
        with self.assertRaises(Exception):
            profile.objects.create(
                game_name="Game 2",
                game_img="https://example.com/g2.jpg",
                game_url="https://unique-url.com/game",
                game_rating=Decimal("7.0"),
                game_price=Decimal("40"),
                game_date=date.today(),
                game_publisher="Publisher 2"
            )

    def test_profile_many_to_many_relationships(self):
        """測試遊戲與平台和分類的多對多關係"""
        platform2 = platform.objects.create(name="PC")
        category2 = category.objects.create(name="RPG")
        
        game = profile.objects.create(
            game_name="Multi Platform Game",
            game_img="https://example.com/multi.jpg",
            game_url="https://store.example.com/multi",
            game_rating=Decimal("8.5"),
            game_price=Decimal("55"),
            game_date=date.today(),
            game_publisher="Studio"
        )
        
        game.platform.add(self.platform, platform2)
        game.category.add(self.category, category2)
        
        self.assertEqual(game.platform.count(), 2)
        self.assertEqual(game.category.count(), 2)


class PlatformSerializerTest(TestCase):
    """平台序列化器測試"""

    def test_platform_serializer_valid_data(self):
        """測試平台序列化器有效數據"""
        data = {'name': 'Mobile'}
        serializer = platformSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_platform_serializer_invalid_data(self):
        """測試平台序列化器無效數據"""
        data = {}
        serializer = platformSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class CategorySerializerTest(TestCase):
    """分類序列化器測試"""

    def test_category_serializer_valid_data(self):
        """測試分類序列化器有效數據"""
        data = {'name': 'Puzzle'}
        serializer = categorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_category_serializer_invalid_data(self):
        """測試分類序列化器無效數據"""
        data = {}
        serializer = categorySerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ProfileSerializerTest(TestCase):
    """遊戲資料序列化器測試"""

    def setUp(self):
        """測試前的準備"""
        self.platform = platform.objects.create(name="Steam")
        self.category = category.objects.create(name="Simulation")

    def test_profile_serializer_valid_data(self):
        """測試遊戲資料序列化器有效數據"""
        game = profile.objects.create(
            game_name="Test Game",
            game_img="https://example.com/test.jpg",
            game_url="https://store.example.com/test",
            game_rating=Decimal("7.5"),
            game_price=Decimal("45"),
            game_date=date.today(),
            game_publisher="Test Publisher"
        )
        game.platform.add(self.platform)
        game.category.add(self.category)

        serializer = profilePostSerializer(game)
        self.assertEqual(serializer.data['game_name'], "Test Game")
        self.assertEqual(serializer.data['game_price'], "45")


class ProfilePostAPITest(APITestCase):
    """遊戲資料 ProfilePost API 測試（核心功能）"""

    def setUp(self):
        """測試前的準備"""
        self.platform = platform.objects.create(name="PC")
        self.category = category.objects.create(name="Action")

    def test_list_all_games(self):
        """測試獲取所有遊戲列表"""
        # 創建測試遊戲
        profile.objects.create(
            game_name="Game 1",
            game_img="https://example.com/g1.jpg",
            game_url="https://store.example.com/game1",
            game_rating=Decimal("8.0"),
            game_price=Decimal("59"),
            game_date=date.today(),
            game_publisher="Publisher 1"
        )

        response = self.client.get('/api/gameprofile/profilePost/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)  # 分頁格式
        self.assertGreater(len(response.data['results']), 0)

    def test_create_game_successfully(self):
        """測試成功創建遊戲"""
        data = {
            'game_name': 'New Game',
            'game_img': 'https://example.com/new.jpg',
            'game_url': 'https://store.example.com/newgame',
            'game_rating': '8.5',
            'game_price': '49',
            'game_date': '2023-03-15',
            'game_publisher': 'New Publisher',
            'platform': 'PC',
            'category': 'Action'
        }

        response = self.client.post('/api/gameprofile/profilePost/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['game_name'], 'New Game')
        self.assertEqual(response.data['game_price'], '49')

    def test_create_game_with_existing_platform_and_category(self):
        """測試使用已存在的平台和分類創建遊戲"""
        data = {
            'game_name': 'Existing Relations Game',
            'game_img': 'https://example.com/exist.jpg',
            'game_url': 'https://store.example.com/exist',
            'game_rating': '8.0',
            'game_price': '45',
            'game_date': '2023-03-15',
            'game_publisher': 'Publisher',
            'platform': 'PC',
            'category': 'Action'
        }

        response = self.client.post('/api/gameprofile/profilePost/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 驗證平台和分類被正確關聯
        self.assertEqual(len(response.data['platform']), 1)
        self.assertEqual(len(response.data['category']), 1)

    def test_create_game_with_multiple_platforms_and_categories(self):
        """測試創建遊戲並關聯多個平台和分類"""
        # 預先創建額外的平台和分類
        platform2 = platform.objects.create(name="PlayStation")
        category2 = category.objects.create(name="RPG")

        data = {
            'game_name': 'Multi-platform Game',
            'game_img': 'https://example.com/multi.jpg',
            'game_url': 'https://store.example.com/multi',
            'game_rating': '8.5',
            'game_price': '59',
            'game_date': '2023-03-15',
            'game_publisher': 'AAA Studio',
            'platform': 'PC,PlayStation',
            'category': 'Action,RPG'
        }

        response = self.client.post('/api/gameprofile/profilePost/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 驗證多個平台
        self.assertEqual(len(response.data['platform']), 2)
        # 驗證多個分類
        self.assertEqual(len(response.data['category']), 2)

    def test_retrieve_single_game(self):
        """測試獲取單個遊戲"""
        game = profile.objects.create(
            game_name="Single Game",
            game_img="https://example.com/single.jpg",
            game_url="https://store.example.com/single",
            game_rating=Decimal("8.5"),
            game_price=Decimal("55"),
            game_date=date.today(),
            game_publisher="Publisher"
        )
        game.platform.add(self.platform)
        game.category.add(self.category)

        response = self.client.get(f'/api/gameprofile/profilePost/{game.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game_name'], "Single Game")
        self.assertEqual(response.data['game_price'], "55")

    def test_update_game_fully(self):
        """測試完全更新遊戲（PUT）"""
        game = profile.objects.create(
            game_name="Original Name",
            game_img="https://example.com/orig.jpg",
            game_url="https://store.example.com/orig",
            game_rating=Decimal("7.0"),
            game_price=Decimal("40"),
            game_date=date.today(),
            game_publisher="Old Publisher"
        )
        game.platform.add(self.platform)
        game.category.add(self.category)

        data = {
            'game_name': 'Updated Name',
            'game_img': 'https://example.com/updated.jpg',
            'game_url': 'https://store.example.com/updated',
            'game_rating': '9.0',
            'game_price': '59',
            'game_date': '2023-06-15',
            'game_publisher': 'New Publisher',
            'platform': 'PC',
            'category': 'Action'
        }

        response = self.client.put(f'/api/gameprofile/profilePost/{game.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game_name'], 'Updated Name')
        self.assertEqual(response.data['game_price'], '59')

    def test_partial_update_game(self):
        """測試部分更新遊戲（PATCH）"""
        game = profile.objects.create(
            game_name="Original Name",
            game_img="https://example.com/orig.jpg",
            game_url="https://store.example.com/orig",
            game_rating=Decimal("7.0"),
            game_price=Decimal("40"),
            game_date=date.today(),
            game_publisher="Old Publisher"
        )

        # 只更新價格
        data = {'game_price': '29'}

        response = self.client.patch(f'/api/gameprofile/profilePost/{game.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game_price'], '29')
        # 驗證其他字段沒變
        self.assertEqual(response.data['game_name'], 'Original Name')

    def test_delete_game(self):
        """測試刪除遊戲"""
        game = profile.objects.create(
            game_name="Delete Me",
            game_img="https://example.com/delete.jpg",
            game_url="https://store.example.com/delete",
            game_rating=Decimal("5.0"),
            game_price=Decimal("10"),
            game_date=date.today(),
            game_publisher="Publisher"
        )

        response = self.client.delete(f'/api/gameprofile/profilePost/{game.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # 驗證遊戲已被刪除
        self.assertFalse(profile.objects.filter(id=game.id).exists())

    def test_search_games_by_name(self):
        """測試搜索遊戲（按名稱）"""
        profile.objects.create(
            game_name="The Legend of Zelda",
            game_img="https://example.com/zelda.jpg",
            game_url="https://store.example.com/zelda",
            game_rating=Decimal("9.5"),
            game_price=Decimal("60"),
            game_date=date.today(),
            game_publisher="Nintendo"
        )

        response = self.client.get('/api/gameprofile/profilePost/?search=Zelda')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)
        self.assertEqual(response.data['results'][0]['game_name'], "The Legend of Zelda")

    def test_search_games_by_publisher(self):
        """測試搜索遊戲（按發行商）"""
        profile.objects.create(
            game_name="EA Game",
            game_img="https://example.com/ea.jpg",
            game_url="https://store.example.com/ea",
            game_rating=Decimal("8.0"),
            game_price=Decimal("50"),
            game_date=date.today(),
            game_publisher="EA Sports"
        )

        response = self.client.get('/api/gameprofile/profilePost/?search=EA')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_games_by_platform(self):
        """測試按平台篩選遊戲"""
        game = profile.objects.create(
            game_name="Platform Specific Game",
            game_img="https://example.com/platform.jpg",
            game_url="https://store.example.com/platform",
            game_rating=Decimal("8.5"),
            game_price=Decimal("55"),
            game_date=date.today(),
            game_publisher="Studio"
        )
        game.platform.add(self.platform)

        response = self.client.get('/api/gameprofile/profilePost/?platform_name=PC')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_games_by_category(self):
        """測試按分類篩選遊戲"""
        game = profile.objects.create(
            game_name="Category Specific Game",
            game_img="https://example.com/category.jpg",
            game_url="https://store.example.com/category",
            game_rating=Decimal("8.0"),
            game_price=Decimal("60"),
            game_date=date.today(),
            game_publisher="Publisher"
        )
        game.category.add(self.category)

        response = self.client.get('/api/gameprofile/profilePost/?category_name=Action')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_games_by_price(self):
        """測試按價格篩選遊戲"""
        profile.objects.create(
            game_name="Expensive Game",
            game_img="https://example.com/exp.jpg",
            game_url="https://store.example.com/exp",
            game_rating=Decimal("9.0"),
            game_price=Decimal("70"),
            game_date=date.today(),
            game_publisher="Premium Publisher"
        )

        response = self.client.get('/api/gameprofile/profilePost/?game_price=70')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_games_by_price_ascending(self):
        """測試按價格升序排列遊戲"""
        profile.objects.create(game_name="G1", game_img="url", game_url="url1", 
                             game_rating=Decimal("7"), game_price=Decimal("30"),
                             game_date=date.today(), game_publisher="P1")
        profile.objects.create(game_name="G2", game_img="url", game_url="url2",
                             game_rating=Decimal("8"), game_price=Decimal("60"),
                             game_date=date.today(), game_publisher="P2")

        response = self.client.get('/api/gameprofile/profilePost/?ordering=game_price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 驗證第一個遊戲的價格更低
        if len(response.data['results']) > 1:
            self.assertLessEqual(
                float(response.data['results'][0]['game_price']),
                float(response.data['results'][1]['game_price'])
            )

    def test_order_games_by_price_descending(self):
        """測試按價格降序排列遊戲"""
        response = self.client.get('/api/gameprofile/profilePost/?ordering=-game_price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        """測試分頁功能"""
        # 創建超過頁面大小的遊戲
        for i in range(15):
            profile.objects.create(
                game_name=f"Game {i}",
                game_img="https://example.com/game.jpg",
                game_url=f"https://store.example.com/game{i}",
                game_rating=Decimal("8.0"),
                game_price=Decimal("50"),
                game_date=date.today(),
                game_publisher="Publisher"
            )

        # 第一頁（默認 12 個）
        response1 = self.client.get('/api/gameprofile/profilePost/?page=1')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response1.data['results']), 12)
        self.assertIsNotNone(response1.data['next'])

        # 第二頁
        response2 = self.client.get('/api/gameprofile/profilePost/?page=2')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response2.data['results']), 0)


class GameProfileAPITest(APITestCase):
    """遊戲資料 API 測試（其他端點）"""

    def setUp(self):
        """測試前的準備"""
        self.platform = platform.objects.create(name="Console")
        self.category = category.objects.create(name="Sports")

    def test_get_platform_list(self):
        """測試獲取平台列表"""
        response = self.client.get('/api/gameprofile/platform/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_list(self):
        """測試獲取分類列表"""
        response = self.client.get('/api/gameprofile/category/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
