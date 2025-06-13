from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify


class UserProfile(AbstractUser):
    first_name = models.CharField(max_length=155)
    last_name = models.CharField(max_length=155)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    bio = CKEditor5Field('Bio')
    location = models.CharField(max_length=155, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.username


class Skill(models.Model):
    name = models.CharField(max_length=155)
    percentage = models.PositiveIntegerField(default=0)
    icon = models.ImageField(upload_to='icons', blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.percentage}"


class Project(models.Model):
    title = models.CharField(max_length=155)
    description = CKEditor5Field('Description')
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='projects/covers/', blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=155)
    content = CKEditor5Field('Content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    tag = models.CharField(max_length=155)
    read_time = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=155, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogContent(models.Model):
    content = CKEditor5Field('Content')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blog_post.title


class Experience(models.Model):
    job_title = models.CharField(max_length=155)
    company = models.CharField(max_length=155)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = CKEditor5Field('Description')

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Education(models.Model):
    school = models.CharField(max_length=155)
    degree = models.CharField(max_length=155)
    teacher = models.CharField(max_length=155)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = CKEditor5Field('Description')

    def __str__(self):
        return f"{self.degree} - {self.school}"


class Message(models.Model):
    name = models.CharField(max_length=155)
    email = models.EmailField()
    subject = models.CharField(max_length=155)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.name}"


class PageViewLog(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} - {self.ip_address}"
