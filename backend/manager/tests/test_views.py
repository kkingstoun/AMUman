from manager.models import Task  # Załóżmy, że mamy model Task
from django.test import Client, TestCase


class AddTaskFormTest(TestCase):
    def setUp(self):
        # Ustawienie klienta testowego
        self.client = Client()
        # self.add_task_url = reverse('/manager/task/add_task/') # Nazwa URL powiązana z widokiem add_task_form
        self.add_task_url = "/manager/task/add_task/"

    def test_add_task_form_get(self):
        # Testowanie odpowiedzi na żądanie GET
        response = self.client.get(self.add_task_url)
        self.assertEqual(response.status_code, 200)

    def test_add_task_form_post(self):
        post_data = {
            "path": "ścieżka/do/pliku.mx3",
            "priority": "normal",
            "gpu_partition": "normal",
            "est": "1",  # Przesyłanie liczby godzin jako ciąg znaków
        }

        response = self.client.post(self.add_task_url, post_data)
        self.assertEqual(
            response.status_code, 302
        )  # Przekierowanie po pomyślnym dodaniu

        self.assertEqual(Task.objects.count(), 1)
        task = Task.objects.first()
        self.assertEqual(task.path, post_data["path"])
        self.assertEqual(task.priority, post_data["priority"])
        self.assertEqual(task.gpu_partition, post_data["gpu_partition"])

        # Sprawdzenie, czy 'est' jest ustawione i porównanie wartości
        if task.est is not None:
            self.assertEqual(task.est, post_data["est"])
        else:
            # Jeśli 'est' jest None, upewnij się, że przesłane 'est' było puste
            self.assertEqual(post_data["est"], "")
