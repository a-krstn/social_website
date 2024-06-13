from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey('auth.User',
                             related_name='actions',
                             on_delete=models.CASCADE)      # юзер, выполнивший действие
    verb = models.CharField(max_length=255)                 # действие, которое выполнил юзер
    created = models.DateTimeField(auto_now_add=True)       # дата и время действия
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE)     # поле указывает на модель ContentType
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True)         # поле для хран-я первич. ключа связ. объекта
    target = GenericForeignKey('target_ct', 'target_id')        # поле для связ. объекта из комбинации полей выше

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['target_ct', 'target_id']),
        ]
        ordering = ['-created']
