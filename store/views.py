from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import ProductSerializer, CartItemSerializer, AddToCartSerializer
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CartView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            items = CartItem.objects.filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)

            total = Decimal('0.00')
            for item in items:
                discount = Decimal(item.product.discount) / Decimal('100')
                discounted_price = item.product.price * (Decimal('1') - discount)
                total += discounted_price * item.quantity

            return Response({
                "items": serializer.data,
                "total": f"{total:.2f}"
            })
        else:
            return Response({"items": [], "total": "0.00"})


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = Product.objects.get(pk=serializer.validated_data['product_id'])
        quantity_to_add = serializer.validated_data['quantity']

        # Verifica disponibilità prodotto
        if product.stock <= 0:
            return Response({"error": f"Prodotto '{product.name}' non disponibile."},
                            status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        new_quantity = item.quantity + quantity_to_add if not created else quantity_to_add

        if new_quantity > product.stock:
            return Response({"error": "Quantità richiesta superiore allo stock disponibile."},
                            status=status.HTTP_400_BAD_REQUEST)

        item.quantity = new_quantity if new_quantity > 0 else 1
        item.save()

        return Response({"message": "Prodotto aggiunto al carrello."}, status=status.HTTP_200_OK)


class UpdateCartQuantityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        if not product_id or quantity is None:
            return Response({"error": "product_id e quantity richiesti."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity)
            if quantity < 0:
                return Response({"error": "La quantità non può essere negativa."},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "La quantità deve essere un numero intero."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Prodotto non trovato."},
                            status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            return Response({"error": "Prodotto non nel carrello."},
                            status=status.HTTP_404_NOT_FOUND)

        # Ora controllo quantità solo se aumento
        if quantity > cart_item.quantity:
            if quantity > product.stock:
                return Response({"error": "Quantità richiesta superiore allo stock disponibile."},
                                status=status.HTTP_400_BAD_REQUEST)

        # Se quantità == 0 elimina l'item
        if quantity == 0:
            cart_item.delete()
            return Response({"message": "Prodotto rimosso dal carrello."}, status=status.HTTP_200_OK)

        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Quantità aggiornata con successo."}, status=status.HTTP_200_OK)

class RemoveFromCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id richiesto."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Prodotto non trovato."}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Prodotto rimosso dal carrello."}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Prodotto non nel carrello."}, status=status.HTTP_404_NOT_FOUND)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response({"error": "Il carrello è vuoto."}, status=status.HTTP_400_BAD_REQUEST)

        # Verifica disponibilità stock
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"Stock insufficiente per il prodotto '{item.product.name}'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Crea ordine
        order = Order.objects.create(user=user, status='pending')

        # Aggiungi prodotti all'ordine e aggiorna stock
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            item.product.stock -= item.quantity
            item.product.save()

        # Svuota il carrello
        cart_items.delete()

        return Response({"message": "Ordine creato con successo."}, status=status.HTTP_201_CREATED)
