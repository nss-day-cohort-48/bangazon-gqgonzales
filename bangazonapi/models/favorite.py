from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE
from .customer import Customer
from .productcategory import ProductCategory
from .orderproduct import OrderProduct


class Favorite(models.Model):
    """The favorite bridge object"""
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING,)
    seller = models.ForeignKey(
        Customer, on_delete=models.DO_NOTHING, related_name='favorited_seller')
