from django.db import IntegrityError, transaction
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Book


@csrf_exempt
def books(request):
    if request.method == 'GET':
        books = Book.objects.all().values()
        books_dict = {'books': list(books)}
        return JsonResponse(books_dict)

    elif request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')

        book = Book(title=title, author=author, price=price)
        try:
            book.save()
        # except IntegrityError as e:
        #     return JsonResponse({'error': str(e),
        #                          'message': 'required field missing'},
        #                         status=400)
        except IntegrityError:
            return JsonResponse({'error': 'true',
                                 'message': 'required field missing'},
                                status=400)
        return JsonResponse(model_to_dict(book), status=201)


@api_view(['GET', 'POST'])
def book(request):
    if request.method == 'POST':
        # We use request.data instead of request.POST.get because we are using the rest_framework
        message = request.data.get('message')
        return Response({'message': f'You sent: {message}'},
                        status=HTTP_201_CREATED)
    return Response("It's done", status=HTTP_200_OK)


# This is a second way to make a class based view
class Orders():
    @staticmethod
    @api_view()
    def listOrders(request):
        return Response({'message': 'list of orders'}, status=HTTP_200_OK)

    # we can make a lot of methods in one class
    # we should use @staticmethod to use them
    @staticmethod
    @api_view(['POST'])
    def createOrder(request):
        if request.method == 'POST':
            ordername = request.data.get('ordername')
            return Response({'message': f'You sent: {ordername}'},
                            status=HTTP_201_CREATED)


# we can direct extend APIView to make a crud api
class BookList(APIView):
    def get(self, request, pk=None):
        if pk:
            # return Response({"message": "single book with id " + str(pk)}, status.HTTP_200_OK)
            book = Book.objects.get(pk=pk)
            return Response(model_to_dict(book), status=HTTP_200_OK)
        else:
            title = request.GET.get('title')
            if title:
                books = Book.objects.filter(title=title)
            else:
                books = Book.objects.all()
            books_dict = {'books': list(books.values())}
            return Response(books_dict, status=HTTP_200_OK)

    def put(self, request, pk):
        # return Response({"title": request.data.get('title')}, status.HTTP_200_OK)

        book = Book.objects.get(pk=pk)
        book.title = request.data.get('title')
        book.author = request.data.get('author')
        book.price = request.data.get('price')
        book.save()
        return Response(model_to_dict(book), status=HTTP_200_OK)

    def post(self, request):
        title = request.data.get('title')
        author = request.data.get('author')
        price = request.data.get('price')
        book = Book(title=title, author=author, price=price)
        try:
            book.save()
        except IntegrityError:
            return Response({'error': 'true',
                             'message': 'required field missing'},
                            status=400)
        return Response(model_to_dict(book), status=HTTP_201_CREATED)


class BookView(APIView):
    def get(self, request, pk=None):
        if pk:
            book = Book.objects.get(pk=pk)
            return Response(model_to_dict(book), status=HTTP_200_OK)
        else:
            books = Book.objects.all()
            books_dict = {'books': list(books.values())}
            return Response(books_dict, status=HTTP_200_OK)

    def put(self, request, pk):
        # we use transaction.atomic() to make sure that the whole operation is done updated or nothing is done
        with transaction.atomic():
            # we can use the update method to update the book
            # Book.objects.filter(pk=pk).update(**request.data)
            # instead of using get and save
            Book.objects.filter(pk=pk).update(title=request.data.get('title'),
                                              author=request.data.get('author'),
                                              price=request.data.get('price'))
            book = Book.objects.get(pk=pk)

            # book = Book.objects.get(pk=pk)
            # book.title = request.data.get('title')
            # book.author = request.data.get('author')
            # book.price = request.data.get('price')
            # book.save()

        return Response(model_to_dict(book), status=HTTP_200_OK)

    def patch(self, request, pk):
        with transaction.atomic():
            book = Book.objects.select_for_update().get(pk=pk)
            book.title = request.data.get('title', book.title)
            book.author = request.data.get('author', book.author)
            book.price = request.data.get('price', book.price)
            update_fields = ["title", "author", "price"]
            book.save(update_fields=update_fields)
        return Response(model_to_dict(book), status=HTTP_200_OK)


class BookViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "All books"}, status.HTTP_200_OK)

    def create(self, request):
        return Response({"message": "Creating a book"}, status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        return Response({"message": "Updating a book"}, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        return Response({"message": "Displaying a book"}, status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return Response({"message": "Partially updating a book"}, status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        return Response({"message": "Deleting a book"}, status.HTTP_200_OK)


# class MenuItemView (generics.ListAPIView, generics.CreateAPIView)
# or we can use ListCreateAPIView
# class MenuItemView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
# This if we want to make a permission for the whole class methods
#     Permission_classes = [IsAuthenticated]


# if we want to make a permission for one or more methods
# we can use/override the permission_classes attribute
#     def get_permissions(self):
#         permission_classes = []
#         if self.request.method != 'GET':
#             permission_classes = [IsAuthenticated]
#         return [permission() for permission in permission_classes]

# Return items for the authenticated user only if the user is authenticated
# class OrderView(generics.ListCreateAPIView):
#      queryset = Order.objects.all()
#      serializer_class = OrderSerializer
#      permission_classes = [IsAuthenticated]
# We can override the get_queryset method to make a filter for the user
#      def get_queryset(self):
#         return Order.objects.all().filter(user=self.request.user)

# returns a simple static response instead of the resources
# class OrderView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     def get(self, request, *args, **kwargs):
#         return Response(‘new response’)

# Though generic views automate everything, you still have full scope to change the default behavior by overriding any of the default methods