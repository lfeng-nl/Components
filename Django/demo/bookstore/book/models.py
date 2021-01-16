from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200)
    datatime = models.DateField()
    Summary = models.TextField()
    img_url = models.URLField()
    authors = models.ManyToManyField('Author', related_name='books')

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    datetime = models.DateTimeField()
    book = models.ForeignKey(Book, related_name='comments')
    content = models.TextField()

    def __str__(self):
        return self.name