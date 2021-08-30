import json
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Customer
# pylint: disable=no-member


class UserTests(APITestCase):
    def setUp(self):
        """
        Create a new account!
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownie.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownie",
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user(self):
        """
        Ensure we can get an existing user.
        """

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/profile")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the customer was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["user"]["last_name"], "Brownie")
