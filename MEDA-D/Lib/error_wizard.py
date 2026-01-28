import os
import sys


# MEDA ERROR WIZARD LIBRARY EXCEPTIONS
class NotFoundSettingsINI(Exception):
    def __init__(self, message):
        self.message = ""
        super().__init__(message)

# Şuanlık geliştirilme aşamasında 1.3 sürümünde eklenmesi planlanıyor...