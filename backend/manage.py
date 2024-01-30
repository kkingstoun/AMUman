#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

SETTINGS_MODULES = {
    'node': "amuman.settings_node",
    'manager': "amuman.settings_manager",
    'client': "amuman.settings_client",
}

if __name__ == "__main__":
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amuman.settings")

    try:
        arg = sys.argv[2]
        os.environ["DJANGO_SETTINGS_MODULE"] = SETTINGS_MODULES.get(arg, "amuman.settings")
    except IndexError:
        pass

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)