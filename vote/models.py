from django.db import models

from rest_framework import serializers

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=254)
    background = models.CharField(max_length=254)
    rank = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=254)
    filename = models.CharField(max_length=254)
    category = models.ForeignKey(Category, related_name='videos')
    description = models.TextField(blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.category.name)


class Student(models.Model):
    hruid = models.CharField(max_length=254, unique=True)
    lastname = models.CharField(max_length=254)
    firstname = models.CharField(max_length=254)
    promo = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s (X%s)" % (self.lastname, self.firstname, self.promo)


class Vote(models.Model):
    student = models.ForeignKey(Student, related_name='votes')
    category = models.ForeignKey(Category, related_name='votes')
    video = models.ForeignKey(Video, related_name='votes')

    class Meta:
        unique_together = ('student', 'category', )

    def __str__(self):
        return "%s a voté pour \"%s\"" % (self.student.__str__(), self.video.__str__())
        

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        extra_kwargs = {
            'student': {'write_only': True},
            'category': {'write_only': True},
            'video': {'write_only': True}
        }

    student_id = serializers.PrimaryKeyRelatedField(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(read_only=True)
    video_id = serializers.PrimaryKeyRelatedField(read_only=True)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        extra_kwargs = {
            'category': {'write_only': True}
        }

    category_id = serializers.PrimaryKeyRelatedField(read_only=True)
    votes = VoteSerializer(read_only=True, many=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

    videos = VideoSerializer(read_only=True, many=True)
    votes = VoteSerializer(read_only=True, many=True)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student

    votes = VoteSerializer(read_only=True, many=True)
