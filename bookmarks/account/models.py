from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    """используется для взаимосвязей пользователей"""
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)     # внеш. ключ для юзера, создающего взаимосвязь
    user_to = models.ForeignKey('auth.User',
                                related_name='re_to_set',
                                on_delete=models.CASCADE)       # внеш. ключ для юзера, на которого есть подписка
    created = models.DateTimeField(auto_now_add=True)           # время создания взаимосвязи

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Добавить следующее поле в User динамически
# параметр symmetrical=False определяет несимметричную взаимосвязь, т.е.
# если user1 подписывается на user2, то это не значит, что user2 автом-чески подписывается на user1
user_model = get_user_model()
user_model.add_to_class('following',
                        models.ManyToManyField('self',
                                               through=Contact,
                                               related_name='followers',
                                               symmetrical=False))
