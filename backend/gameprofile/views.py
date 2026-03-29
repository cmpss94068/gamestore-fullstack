from rest_framework import viewsets, pagination, status
from .serializers import profilePostSerializer, platformSerializer, categorySerializer
from .models import profile, platform, category
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProfileFilter

# Create your views here.
class platformView(viewsets.ModelViewSet):
    queryset = platform.objects.all().order_by('id')
    serializer_class = platformSerializer

class categoryView(viewsets.ModelViewSet):
    queryset = category.objects.all().order_by('id')
    serializer_class = categorySerializer

class customPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'

class profilePostView(viewsets.ModelViewSet):
    queryset = profile.objects.all()
    serializer_class = profilePostSerializer
    filterset_class = ProfileFilter
    pagination_class = customPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['game_publisher', 'game_date', 'game_price']
    search_fields = ['game_name', 'game_publisher']
    ordering_fields = ['game_date', 'game_price']

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_kwargs = {}
        platforms = self.request.GET.get('platform_name', None)
        categories = self.request.GET.get('category_name', None)
        if platforms:
            platforms = platforms.split(',')
            filter_kwargs['platform__name__in'] = platforms
        if categories:
            categories = categories.split(',')
            filter_kwargs['category__name__in'] = categories
        return queryset.filter(**filter_kwargs)

    def create(self, request, *args, **kwargs):
        from .models import category, platform
        new_cate = []
        new_plat = []
        for category_name in request.data['category'].split(','):
            try:
                cate = category.objects.get(name=category_name)
                new_cate.append(cate)
            except category.DoesNotExist:
                cate = category.objects.create(name=category_name)
                new_cate.append(cate)

        for platform_name in request.data['platform'].split(','):
            try:
                plat = platform.objects.get(name=platform_name)
                new_plat.append(plat)
            except platform.DoesNotExist:
                plat = platform.objects.create(name=platform_name)
                new_plat.append(plat)

        post_obj = profile.objects.create(
            game_name = request.data['game_name'],
            game_img = request.data['game_img'],
            game_url = request.data['game_url'],
            game_rating = request.data['game_rating'],
            game_price = request.data['game_price'],
            game_date = request.data['game_date'],
            game_publisher = request.data['game_publisher'],
        )

        post_obj.category.add(*new_cate)
        post_obj.platform.add(*new_plat)

        # 創建序列化器實例來序列化數據（不保存，因為已經創建了）
        serializer = self.serializer_class(post_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.get('partial', False)
        
        # 處理平台和分類的字串
        new_cate = []
        new_plat = []
        
        if 'category' in request.data:
            for category_name in request.data['category'].split(','):
                try:
                    cate = category.objects.get(name=category_name.strip())
                    new_cate.append(cate)
                except category.DoesNotExist:
                    cate = category.objects.create(name=category_name.strip())
                    new_cate.append(cate)
        
        if 'platform' in request.data:
            for platform_name in request.data['platform'].split(','):
                try:
                    plat = platform.objects.get(name=platform_name.strip())
                    new_plat.append(plat)
                except platform.DoesNotExist:
                    plat = platform.objects.create(name=platform_name.strip())
                    new_plat.append(plat)
        
        # Update the instance fields
        if not partial or 'game_name' in request.data:
            instance.game_name = request.data.get('game_name', instance.game_name)
        if not partial or 'game_img' in request.data:
            instance.game_img = request.data.get('game_img', instance.game_img)
        if not partial or 'game_url' in request.data:
            instance.game_url = request.data.get('game_url', instance.game_url)
        if not partial or 'game_rating' in request.data:
            instance.game_rating = request.data.get('game_rating', instance.game_rating)
        if not partial or 'game_price' in request.data:
            instance.game_price = request.data.get('game_price', instance.game_price)
        if not partial or 'game_date' in request.data:
            instance.game_date = request.data.get('game_date', instance.game_date)
        if not partial or 'game_publisher' in request.data:
            instance.game_publisher = request.data.get('game_publisher', instance.game_publisher)
        
        instance.save()
        
        # Update many-to-many relationships
        if new_cate:
            instance.category.clear()
            instance.category.add(*new_cate)
        if new_plat:
            instance.platform.clear()
            instance.platform.add(*new_plat)
        
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)