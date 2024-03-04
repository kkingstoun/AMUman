import random

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class JobManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_username = "admin"
        self.admin_password = "admin"
        # Sprawdź, czy użytkownik admin istnieje, a jeśli nie, utwórz go
        user = get_user_model()
        if not user.objects.filter(username=self.admin_username).exists():
            user.objects.create_superuser(
                self.admin_username, "admin@example.com", self.admin_password
            )
        self.job_url = "/api/jobs/"  # Upewnij się, że to jest poprawny URL endpointu

    def test_login_and_create_jobs(self):
        # Użyj tokena dla uwierzytelnienia zamiast logowania, jeśli Twoje API tak wymaga
        login_response = self.client.login(
            username=self.admin_username, password=self.admin_password
        )
        self.assertTrue(login_response)
        # Dla tokena (zakładając, że masz endpoint do logowania i otrzymywania tokena):
        login_response = self.client.post(
            "/api/token/",
            {"username": self.admin_username, "password": self.admin_password},
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Create 3 jobs with random values
        for _ in range(3):
            job_data = {
                "user": "test_user_" + str(random.randint(1, 100)),
                "path": "/path/to/simulation_" + str(random.randint(1, 100)),
                "node_name": "node_" + str(random.randint(1, 10)),
                "port": random.randint(8000, 9000),
                "priority": random.choice(["LOW", "NORMAL", "HIGH"]),
                "gpu_partition": random.choice(["SLOW", "NORMAL", "FAST"]),
                "duration": random.randint(1, 100),
                "status": "PENDING",
            }
            response = self.client.post(self.job_url, job_data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
