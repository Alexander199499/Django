from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse



class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        rating_of_posts_by_author = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_comments_by_author = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_under_posts_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_of_posts_by_author + rating_of_comments_by_author + rating_of_comments_under_posts_of_author
        self.save()


class Category(models.Model):
    culture = 'CU'
    cience = 'SC'
    tech = 'TE'
    politics = 'PO'
    sport = 'SP'
    entertainment = 'EN'
    economics = 'EC'
    education = 'ED'

    CATEGORIES = [
        (culture, 'Культура'),
        (cience, 'Наука'),
        (tech, 'Технология'),
        (politics, 'Политика'),
        (sport, 'Спорт'),
        (entertainment, 'Развлечения'),
        (economics, 'Экономика'),
        (education, 'Образование')
    ]

    news_category = models.CharField(unique=True, max_length=2, choices=CATEGORIES)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.get_news_category_display()


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    time_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.title()}: {self.text[:10]}'

    def get_absolute_url(self):
        return reverse('postdetail', args=[str(self.id)])


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_created = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
