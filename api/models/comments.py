from django.db import models
from django.contrib.auth import get_user_model

from .review import Review


User = get_user_model()


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        verbose_name='Comments',
    )
    text = models.CharField(max_length=255, verbose_name='Text')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Publication date',
    )

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return ': '.join(
            [str(self.pub_date), str(self.author), self.text[:15] + '...'])
