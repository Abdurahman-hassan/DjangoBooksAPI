from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

# Using SimpleRouter
simple_router = SimpleRouter(trailing_slash=False)
simple_router.register('simple-books', views.BookViewSet, basename='simple-books')

# Using DefaultRouter
default_router = DefaultRouter(trailing_slash=False)
default_router.register('default-books', views.BookViewSet, basename='default-books')
# using simple_router.urls or default_router.urls will return a list of urls
# urlpatterns = default_router.urls


urlpatterns = [
    # simple view
    path('books', views.books, name='books'),

    # basic APIView
    path('book', views.book, name='book'),
    path('orders', views.Orders.listOrders, name='orders'),
    path('orders/create', views.Orders.createOrder, name='create-order'),
    path('books-manual-view', views.BookList.as_view(), name='bookList'),
    path('books-manual-view/<int:pk>', views.BookList.as_view(), name='bookList-detail'),
    path('books-simple-view', views.BookView.as_view(), name='book-simple-view'),
    path('books-simple-view/<int:pk>', views.BookView.as_view(), name='book-simple-view-detail'),

    path('bookviewset-manual', views.BookViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        })),

    path('bookviewset-manual/<int:pk>', views.BookViewSet.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })),

    path('get-simple-router/', include(simple_router.urls)),
    path('get-default-router/', include(default_router.urls))

]
