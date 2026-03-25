from rest_framework import viewsets, pagination
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

        serializer = self.serializer_class(post_obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)