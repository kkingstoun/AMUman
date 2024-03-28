import logging

from django.contrib.auth.models import User as AuthUser
from django.core.exceptions import MiddlewareNotUsed

from manager.models import CustomUser

log = logging.getLogger("rich")


class Generate:
    def __init__(self, get_response):
        self.get_response = get_response
        self.generate_users()
        raise MiddlewareNotUsed("Generate is disabled after initial use.")

    def generate_users(self):
        if not CustomUser.objects.exists():
            admin = AuthUser.objects.get(username="admin")
            self.admin_user = CustomUser(auth=admin, concurrent_jobs=20)
            self.admin_user.save()

    def __call__(self, request):
        response = self.get_response(request)
        return response
