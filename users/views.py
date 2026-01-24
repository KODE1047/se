# users/views.py
from rest_framework import viewsets, permissions, status, decorators
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegistrationSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create': 
            # Req 4-1: Admin creates staff, but we also need public registration for students
            return [permissions.AllowAny()] 
        return [permissions.IsAuthenticated()]

    @decorators.action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Req 1-1: Student Registration"""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(role='STUDENT')
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @decorators.action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def toggle_status(self, request, pk=None):
        """Req 3-7: Staff/Admin activate or deactivate student"""
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        status_msg = "Activated" if user.is_active else "Deactivated"
        return Response({"status": status_msg})