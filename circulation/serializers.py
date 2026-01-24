# circulation/serializers.py
from rest_framework import serializers
from .models import Loan
from catalog.models import BookCopy

class LoanCreateSerializer(serializers.ModelSerializer):
    inventory_code = serializers.CharField(write_only=True)

    class Meta:
        model = Loan
        fields = ['id', 'inventory_code', 'due_date']
        read_only_fields = ['id', 'due_date']

    def validate_inventory_code(self, value):
        try:
            copy = BookCopy.objects.get(inventory_code=value)
            if copy.status != 'AVAILABLE':
                raise serializers.ValidationError("This copy is not available for checkout.")
            return copy
        except BookCopy.DoesNotExist:
            raise serializers.ValidationError("Invalid Inventory Code.")

    def create(self, validated_data):
        copy = validated_data['inventory_code']
        user = self.context['request'].user
        
        # Create Loan
        loan = Loan.objects.create(user=user, copy=copy)
        
        # Update Copy Status
        copy.status = 'BORROWED'
        copy.save()
        
        return loan

class LoanDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='copy.book.title')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Loan
        fields = ['id', 'user_email', 'book_title', 'checkout_date', 'due_date', 'return_date', 'status']