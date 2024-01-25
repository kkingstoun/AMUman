#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # Sprawdzenie, czy drugi argument (tryb) jest podany
    if len(sys.argv) > 2:
        mode = sys.argv[1]
        if mode in ["client", "node", "master"]:
            # Ustawienie odpowiedniego pliku ustawień
            settings_module = f"amuman.settings_{mode}"
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
            sys.argv.pop(1)  # Usunięcie argumentu trybu z argv
        else:
            raise ValueError("Nieznany tryb: wybierz 'client', 'node' lub 'master'")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amuman.settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
