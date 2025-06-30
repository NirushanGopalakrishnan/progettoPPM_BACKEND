from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Cart, CartItem
from .serializers import ProductSerializer, CartItemSerializer, AddToCartSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CartView(APIView):
    # Accesso pubblico, carrello visibile solo se utente loggato
    def get(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)

            # Calcola totale carrello
            total = sum(item.product.price * item.quantity for item in items)
            return Response({
                "items": serializer.data,
                "total": f"{total:.2f}"
            })
        else:
            return Response({"items": [], "total": "0.00"})


class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=serializer.validated_data['product_id'])
        quantity_to_add = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        new_quantity = item.quantity + quantity_to_add if not created else quantity_to_add

        if new_quantity > product.stock:
            return Response({"error": "Quantità richiesta superiore allo stock disponibile."},
                            status=status.HTTP_400_BAD_REQUEST)

        item.quantity = new_quantity if new_quantity > 0 else 1
        item.save()

        return Response({"message": "Prodotto aggiunto al carrello."}, status=status.HTTP_200_OK)
