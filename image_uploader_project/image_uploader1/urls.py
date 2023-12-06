from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ImageViewSet, ImageView
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('api2/', include(router.urls)),
    path('api/images/', ImageView.as_view(), name='image-upload')
    

    # Add your custom URL patterns here
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)