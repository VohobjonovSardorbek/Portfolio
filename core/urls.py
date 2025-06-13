from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import token_obtain_pair , token_refresh
from django.conf import settings
from django.conf.urls.static import static

from main.views import *

schema_view = get_schema_view(
   openapi.Info(
      title="Portfolio API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns += [
    path('users/', UserListAPIView.as_view(), name='users-list'),

    path('skills/', SkillListAPIView.as_view(), name='skills-list'),
    path('skill/create/', SkillCreateAPIView.as_view(), name='skills-create'),
    path('skill/<int:pk>/', SkillDetailAPIView.as_view(), name='skill-detail'),

    path('projects/', ProjectListAPIView.as_view(), name='project-list'),
    path('project/create/', ProjectCreateAPIView.as_view(), name='project-create'),
    path('project/<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),

    path('blogs/', BlogPostListAPIView.as_view(), name='blog-list'),
    path('blog/create/', BlogPostCreateAPIView.as_view(), name='blog-create'),
    path('blog/<slug:slug>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
    path('blog/<slug:slug>/update/', BlogPostUpdateAPIView.as_view(), name='blog-update'),
    path('blog/<slug:slug>/delete/', BlogPostDeleteAPIView.as_view(), name='blog-delete'),

    path('blog-contents/', BlogContentListAPIView.as_view(), name='blog-content-list'),
    path('blog-content/create/', BlogContentCreateAPIView.as_view(), name='blog-content-create'),
    path('blog-content/<int:pk>/', BlogContentDetailAPIView.as_view(), name='blog-content-detail'),

    path('experiences/', ExperienceListAPIView.as_view(), name='experience-list'),
    path('experience/create/', ExperienceCreateAPIView.as_view(), name='experience-create'),
    path('experience/<int:pk>/', ExperienceDetailAPIView.as_view(), name='experience-detail'),

    path('educations/', EducationListAPIView.as_view(), name='education-list'),
    path('education/create/', EducationCreateAPIView.as_view(), name='education-create'),
    path('education/<int:pk>/', EducationDetailAPIView.as_view(), name='education-detail'),

    path('messages/', MessageListAPIView.as_view(), name='message-list'),
    path('message/create/', MessageCreateAPIView.as_view(), name='message-create'),
    path('message/<int:pk>/', MessagesDetailAPIView.as_view(), name='message-detail'),

    path('page-view/create/', PageViewLogCreateAPIView.as_view(), name='page-view-create'),
    path('page-views/', PageViewLogListAPIView.as_view(), name='page-view-list'),
]

urlpatterns += [
    path('token/', token_obtain_pair ),
    path('token/refresh/', token_refresh ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

