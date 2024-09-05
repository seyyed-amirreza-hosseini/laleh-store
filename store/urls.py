from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')  # products-list, products-detail
router.register('collections', views.CollectionViewSet)

producst_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
producst_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

urlpatterns = router.urls + producst_router.urls
