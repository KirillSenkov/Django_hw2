from django.db import models

class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title + ' (' + str(self.published_at) + ')'


class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    def __str__(self):
        return self.name


class Scope(models.Model):
    article_id = models.ForeignKey(Article, related_name='scope',
                                   on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, related_name='tags', verbose_name='Тэг',
                               on_delete=models.CASCADE)

    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = 'Тематики статьи'
        unique_together = ['tag_id', 'article_id']

        constraints = [
            models.UniqueConstraint(
                fields=['article_id'],
                name='unique_main_tag_per_article',
                condition=models.Q(is_main=True)
            )
        ]
