"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
# from bangazonapi.models import Product
from bangazonreports.views import Connection


def expensive_products_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT p.id,
                    p.name AS product_name,
                    p.price,
                    p.description,
                    p.quantity,
                    p.created_date,
                    p.category_id,
                    p.location,
                    p.image_path
                FROM bangazonapi_product p
                WHERE p.price >= 1000
                ORDER BY p.price ASC
            """)

            dataset = db_cursor.fetchall()

            expensive_products = {}

            for row in dataset:

                expensive_products[row['id']] = {}
                expensive_products[row['id']]['id'] = row["id"]
                expensive_products[row['id']
                                   ]["description"] = row["description"]
                expensive_products[row['id']]['name'] = row["product_name"]
                expensive_products[row['id']]['price'] = row["price"]

        # Get only the values from the dictionary and create a list from them
        list_of_expensive_products = expensive_products.values()

        # Specify the Django template and provide data context
        template = 'products/list_with_expensive_products.html'
        context = {
            'expensive_products_list': list_of_expensive_products
        }

        return render(request, template, context)
