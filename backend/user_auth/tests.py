from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import RegisterationSerializer


class UserRegistrationSerializerTest(TestCase):
    """用戶註冊序列化器測試"""

    def test_valid_registration_data(self):
        """測試有效的註冊數據"""
        data = {
            'username': 'newuser',
            'password': 'SecurePassword123',
            'password2': 'SecurePassword123'
        }
        serializer = RegisterationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """測試密碼不匹配"""
        data = {
            'username': 'newuser',
            'password': 'SecurePassword123',
            'password2': 'DifferentPassword123'
        }
        serializer = RegisterationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_missing_username(self):
        """測試缺少用戶名"""
        data = {
            'password': 'SecurePassword123',
            'password2': 'SecurePassword123'
        }
        serializer = RegisterationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_weak_password_no_uppercase(self):
        """測試密碼沒有大寫字母"""
        data = {
            'username': 'newuser',
            'password': 'insecurepassword123',
            'password2': 'insecurepassword123'
        }
        serializer = RegisterationSerializer(data=data)
        # 會被序列化驗證器檢查
        self.assertFalse(serializer.is_valid())

    def test_weak_password_no_lowercase(self):
        """測試密碼沒有小寫字母"""
        data = {
            'username': 'newuser',
            'password': 'INSECUREPASSWORD123',
            'password2': 'INSECUREPASSWORD123'
        }
        serializer = RegisterationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_weak_password_no_digit(self):
        """測試密碼沒有數字"""
        data = {
            'username': 'newuser',
            'password': 'InsecurePassword',
            'password2': 'InsecurePassword'
        }
        serializer = RegisterationSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class UserRegistrationAPITest(APITestCase):
    """用戶註冊 API 測試"""

    def test_successful_user_registration(self):
        """測試成功的用戶註冊"""
        data = {
            'username': 'testuser',
            'password': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_duplicate_username_registration(self):
        """測試重複用戶名註冊"""
        User.objects.create_user(username='existinguser', password='TestPassword123')
        
        data = {
            'username': 'existinguser',
            'password': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        
        # 會因為用戶名已存在而失敗
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_mismatched_passwords(self):
        """測試密碼不匹配的註冊"""
        data = {
            'username': 'newuser',
            'password': 'TestPassword123',
            'password2': 'DifferentPassword123'
        }
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_with_weak_password(self):
        """測試弱密碼的註冊"""
        data = {
            'username': 'newuser',
            'password': 'weak',
            'password2': 'weak'
        }
        response = self.client.post('/api/register/', data, format='json')
        
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users_list(self):
        """測試獲取用戶列表"""
        User.objects.create_user(username='user1', password='TestPassword123')
        User.objects.create_user(username='user2', password='TestPassword123')
        
        response = self.client.get('/api/auth/register/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserModelTest(TestCase):
    """用戶模型測試"""

    def test_create_user_successfully(self):
        """測試成功創建用戶"""
        user = User.objects.create_user(
            username='testuser',
            password='TestPassword123'
        )
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(user.check_password('TestPassword123'))

    def test_user_password_hashing(self):
        """測試用戶密碼是否被正確加密"""
        user = User.objects.create_user(
            username='hashuser',
            password='TestPassword123'
        )
        self.assertNotEqual(user.password, 'TestPassword123')
        self.assertTrue(user.check_password('TestPassword123'))

    def test_user_authentication(self):
        """測試用戶認證"""
        user = User.objects.create_user(
            username='authuser',
            password='TestPassword123'
        )
        authenticated = User.objects.get(username='authuser')
        self.assertEqual(authenticated.username, 'authuser')
