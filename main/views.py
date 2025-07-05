from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.generics import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, SAFE_METHODS


class UserListAPIView(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer


class SkillListAPIView(ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]


class SkillCreateAPIView(CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


class SkillDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]


class ProjectListAPIView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]


class ProjectCreateAPIView(CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]


class ProjectDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]


class BlogPostListAPIView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogPostDetailAPIView(RetrieveAPIView):
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.all()
    lookup_field = 'slug'


class BlogPostCreateAPIView(CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        instance = serializer.save()
        if not instance.slug:
            instance.slug = slugify(instance.title)
            instance.save()


class BlogPostUpdateAPIView(UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'


class BlogPostDeleteAPIView(DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'


class BlogContentListAPIView(ListAPIView):
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSafeSerializer


class BlogContentCreateAPIView(CreateAPIView):
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer


class BlogContentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer


class ExperienceListAPIView(ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ExperienceCreateAPIView(CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ExperienceDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class EducationListAPIView(ListAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class EducationCreateAPIView(CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class EducationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class MessageListAPIView(ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageCreateAPIView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessagesDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class PageViewLogListAPIView(ListAPIView):
    queryset = PageViewLog.objects.all()
    serializer_class = PageViewLogSerializer


class PageViewLogCreateAPIView(APIView):

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['project'],
            properties={
                'project': openapi.Schema(type=openapi.TYPE_INTEGER, description='Project ID')
            },
        ),
        responses={201: PageViewLogSerializer()}
    )
    def post(self, request, format=None):
        project_id = request.data.get('project')
        ip_address = self.get_client_ip(request)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

        log = PageViewLog.objects.create(project=project, ip_address=ip_address)
        serializer = PageViewLogSerializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
