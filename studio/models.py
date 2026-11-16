from django.db import models


class Master(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Design(models.Model):
    title = models.CharField(max_length=150)
    style = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    image_url = models.URLField()
    master = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name="designs",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
