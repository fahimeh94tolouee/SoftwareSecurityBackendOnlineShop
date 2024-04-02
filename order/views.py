from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from Backend_Shop.utils import generate_response_messages
from product.models import Product
from .models import Cart, CartItem
from .serializers import CartItemSerializer


@api_view(['POST'])
def add_to_cart(request):
    """
    Add a product to the user's cart.
    """
    # Retrieve user from the request
    user = request.user

    # Extract product ID from the request data
    product_id = request.data.get('id')

    # Check if the product exists
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(generate_response_messages("Product does not exist"), status=status.HTTP_400_BAD_REQUEST)

    # Check if the user already has the product in their cart
    cart, created = Cart.objects.get_or_create(user=user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # If the item is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the item is not in the cart, create a new CartItem instance
        cart_item = CartItem(cart=cart, product=product)
        cart_item.save()

    # Serialize the cart item and return the response
    serializer = CartItemSerializer(cart_item)
    return Response({
        "data": serializer.data,
        **generate_response_messages("Product added to cart successfully.")
    }, status=status.HTTP_201_CREATED)
