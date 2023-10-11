from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_children(self):
        return Menu.objects.filter(parent=self)

    def is_active(self, current_url):
        return current_url == self.url
    