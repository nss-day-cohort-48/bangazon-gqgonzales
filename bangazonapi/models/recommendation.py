from django.db import models
from .customer import Customer
from .product import Product


class Recommendation(models.Model):

    customer = models.ForeignKey(
        Customer, related_name='incoming_recs', on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
    recommender = models.ForeignKey(
        Customer, related_name='outgoing_recs', on_delete=models.DO_NOTHING,)
