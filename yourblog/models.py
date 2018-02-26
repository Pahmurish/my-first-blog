from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField




class KeyWords(models.Model):
    class Meta():
        db_table = 'keywords'
    name = models.CharField(max_length=50, unique=True, verbose_name='Теги')

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    title = models.CharField(max_length=200)
    text = RichTextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    #post_img = models.ImageField(verbose_name='Картинка', upload_to='')
    keywords = models.ManyToManyField(KeyWords, related_name="keywords", related_query_name="keyword",
                                      verbose_name=u'Теги')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('yourblog.Post', related_name='comments', on_delete=models.CASCADE,)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

