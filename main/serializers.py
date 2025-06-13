from .models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        ]


class SkillSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
            'percentage',
            'icon'
        ]


class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    cover_image = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'image',
            'cover_image',
            'project_url',
            'created_at'
        ]


class BlogPostSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'content',
            'is_published',
            'cover_image',
            'created_at',
            'updated_at',
            'tag',
            'read_time',
            'slug',
        ]


class BlogPostShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title']


class BlogContentSafeSerializer(serializers.ModelSerializer):
    blog_post = BlogPostShortSerializer(read_only=True)

    class Meta:
        model = BlogContent
        fields = [
            'id',
            'content',
            'blog_post',
            'created_at',
        ]


class BlogContentSerializer(serializers.ModelSerializer):
    blog_post_id = serializers.PrimaryKeyRelatedField(
        queryset=BlogPost.objects.all(), write_only=True, source='blog_post'
    )

    class Meta:
        model = BlogContent
        fields = [
            'id',
            'content',
            'blog_post_id',
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format='%Y-%m-%d', input_formats=('%Y-%m-%d',))
    end_date = serializers.DateField(format='%Y-%m-%d', input_formats=('%Y-%m-%d',), required=False, allow_null=True)

    class Meta:
        model = Experience
        fields = [
            'id',
            'job_title',
            'company',
            'start_date',
            'end_date',
            'description'
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'school',
            'degree',
            'teacher',
            'start_year',
            'end_year',
            'description',
        ]


class MessageSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    read_at = serializers.BooleanField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'name',
            'email',
            'subject',
            'message',
            'read_at',
            'created_at',
        ]


class PageViewLogSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PageViewLog
        fields = [
            'id',
            'project',
            'project_id',
            'ip_address',
            'timestamp'
        ]
