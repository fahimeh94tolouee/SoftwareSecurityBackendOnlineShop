from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Backend_Shop.utils import generate_response_messages, convert_dict_to_array
from .models import Product, ProductQuestion
from .serializers import ProductSerializer, ProductQuestionSerializer, ProductQuestionCreateSerializer, \
    ProductAnswerCreateSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def getList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response({
        "data": serializer.data,
        **generate_response_messages("Get product list successfully.")
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def show(request, id):
    # Retrieve the product with the specified ID or return 404 if not found
    product = get_object_or_404(Product, id=id)
    serializer = ProductSerializer(product)
    return Response({
        "data": serializer.data,
        **generate_response_messages("Get product successfully.")
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_questions_list(request, product_id):
    """
    List all questions and their answers for a specific product.
    """
    questions = ProductQuestion.objects.filter(product_id=product_id)
    serializer = ProductQuestionSerializer(questions, many=True)
    return Response({
        "data": serializer.data,
        **generate_response_messages("Get questions for the product successfully.")
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request, product_id):
    """
    Create a new question for a product.
    """
    try:
        # Retrieve the product instance
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return Response(generate_response_messages("Product does not exist."), status=status.HTTP_404_NOT_FOUND)

    # Access the authenticated user from the request
    user = request.user

    # Create the serializer instance with product and user passed as context
    serializer = ProductQuestionCreateSerializer(data=request.data, context={'user': user, 'product': product})
    if serializer.is_valid():
        serializer.save()
        return Response({
            "data": serializer.data,
            **generate_response_messages("Question is created successfully.")
        }, status=status.HTTP_201_CREATED)
    else:
        error_messages = convert_dict_to_array(serializer.errors)
        # Pass error messages through generate_response_messages function
        error_messages = generate_response_messages(error_messages)
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_answer(request):
    """
    Create a new answer for a product question.
    """
    # Retrieve the authenticated user from the request
    user = request.user

    # Retrieve question ID from request data
    question_id = request.data.get('question_id')

    # Check if the question exists
    try:
        question = ProductQuestion.objects.get(id=question_id)
    except ProductQuestion.DoesNotExist:
        return Response(generate_response_messages("Question does not exist"), status=status.HTTP_400_BAD_REQUEST)

    # Create the serializer instance with user and question passed as context
    serializer = ProductAnswerCreateSerializer(data=request.data, context={'user': user, 'question': question})
    if serializer.is_valid():
        serializer.save()
        return Response({
            "data": serializer.data,
            **generate_response_messages("Answer is stored successfully.")
        }, status=status.HTTP_201_CREATED)
    else:
        error_messages = convert_dict_to_array(serializer.errors)
        # Pass error messages through generate_response_messages function
        error_messages = generate_response_messages(error_messages)
        return Response(error_messages, status=status.HTTP_400_BAD_REQUEST)