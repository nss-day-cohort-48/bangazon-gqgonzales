from django.urls import path
from .views import expensive_products_list

urlpatterns = [
    path('reports/expensiveproducts', expensive_products_list),
]
