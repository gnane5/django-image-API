from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile, Image
from .serializers import UserProfileSerializer, ImageSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
# Create your views here.


class UserProfileViewSet(viewsets.ModelViewSet):    
    queryset = UserProfile.objects.all()[1:5]
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def user_images(self, request):
        images = Image.objects.filter(user=request.user)
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

class CompanyViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

@csrf_exempt
class MyTokenObtainPairView(TokenObtainPairView):
    pass

class MyTokenRefreshView(TokenRefreshView):
    # Customization can be added here if needed
    pass


class ImageView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = self.request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)