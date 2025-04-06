from django.db import models
from django.utils import timezone

class Edge(models.Model):
    x1 = models.BigIntegerField()
    y1 = models.BigIntegerField()
    x2 = models.BigIntegerField()
    y2 = models.BigIntegerField()
    def __str__(self):
        """Returns a string representation of a message."""
        return f"'{str(self.x1)}':'{str(self.y1)}', '{str(self.x2)}':'{str(self.y2)}'"
