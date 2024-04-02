from rest_framework import serializers

from Backend_Shop.utils import generate_response_messages
from .models import Product, ProductQuestion, ProductAnswer


class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()

    def get_colors(self, obj):
        return [color.name for color in obj.colors.all()]

    class Meta:
        model = Product
        fields = ['id', 'title', 'image_path', 'price', 'tags', 'category', 'type', 'vendor', 'description', 'colors']


class ProductAnswerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%B %d, %Y')

    class Meta:
        model = ProductAnswer
        fields = ['id', 'user', 'answer', 'likes', 'dislikes', 'created_at']

    def get_user(self, obj):
        if obj.anonymous:
            return "Anonymous"
        return f"{obj.user.first_name} {obj.user.last_name}"


class ProductQuestionSerializer(serializers.ModelSerializer):
    answers = ProductAnswerSerializer(many=True, read_only=True)  # Include answers field
    user = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%B %d, %Y')

    class Meta:
        model = ProductQuestion
        fields = ['id', 'user', 'question', 'likes', 'dislikes', 'created_at', 'answers']

    def get_user(self, obj):
        if obj.anonymous:
            return "Anonymous"
        return f"{obj.user.first_name} {obj.user.last_name}"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        answers = ProductAnswer.objects.filter(question=instance)
        answer_data = ProductAnswerSerializer(answers, many=True).data
        representation['answers'] = answer_data
        return representation


class ProductQuestionCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductQuestion
        fields = ['id', 'user', 'question', 'likes', 'dislikes', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        question = data.get('question')
        if not question:
            raise serializers.ValidationError(generate_response_messages("Question cannot be empty."))
        return data

    def create(self, validated_data):
        """
        Create and return a new ProductQuestion instance, associating it with the authenticated user.
        """
        user = self.context['user']
        product = self.context['product']
        validated_data['user'] = user
        validated_data['product'] = product
        return super().create(validated_data)


class ProductAnswerCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # created_at = serializers.DateTimeField(format='%B %d, %Y')

    class Meta:
        model = ProductAnswer
        fields = ['id', 'user', 'question', 'answer', 'likes', 'dislikes', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        """
        Create and return a new ProductAnswer instance, associating it with the authenticated user.
        """
        user = self.context['user']  # Retrieve the user from the context
        validated_data['user'] = user  # Set the user for the answer
        return super().create(validated_data)
