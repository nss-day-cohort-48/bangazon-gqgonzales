import json
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Order, OrderProduct, Payment


class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = {"name": "Kite", "price": 14.99, "quantity": 60,
                "description": "It flies high", "category_id": 1, "location": "Pittsburgh"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        product = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a payment type, instantiate it
        payment_type = Payment()
        payment_type.merchant_name = "Discover Card"
        payment_type.account_number = "1111111111"
        payment_type.expiration_date = "2025-10-10"
        payment_type.create_date = "2020-01-01"
        payment_type.customer_id = 1
        payment_type.save()

        # Create an order / add a product to it
        order = Order()
        order.customer_id = 1
        order.payment_type_id = None
        order.created_date = "2021-05-05"
        order.save()

        lineitem = OrderProduct()
        lineitem.order = order
        lineitem.product_id = product["id"]
        lineitem.save()

    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = {"product_id": 1}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["size"], 2)
        self.assertEqual(len(json_response["lineitems"]), 2)

    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = {"product_id": 1}
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)

    def test_complete_order_with_payment_type(self):
        """
        Test to make sure orders are being closed as a payment type is added.
        """

        # Create a payment type
        # Already accomplished in set up

        # Add that created payment type to the cart with PUT
        data = {"payment_type": 1}

        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put("/orders/1", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # SO, to fix this test, you COULD change this to a 404...but that doesn't feel right

        # Get cart and veryify payment type has been added
        response = self.client.get("/orders/1", None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["payment_type"]["id"], 1)

    # Create test that verifies that adding a product to the user's cart adds it to an open order
    # and not a closed one.
    def test_only_add_products_to_open_carts(self):
        """
        Test that verifies that adding a product to the user's cart adds it to an open order and not a closed one.
        """
        data = {"payment_type": 1}

        # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put("/orders/1", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and veryify payment type has been added
        response = self.client.get("/orders/1", None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["payment_type"]["id"], 1)

        response = self.client.get("/profile/cart", None, format="json")
        json_response = json.loads(response.content)

        # Cool, now add a new product to the database
        url = "/products"
        data = {"name": "Scooter", "price": 800, "quantity": 12,
                "description": "Moves fast!", "category_id": 1, "location": "Nashville"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # And add new product to cart
        url = "/cart"
        data = {"product_id": 2}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Finally, check the cart to see the contents.
        # Should only have 1 item.
        url = "/cart"
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 2)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)
