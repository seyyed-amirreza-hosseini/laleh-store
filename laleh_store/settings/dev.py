from .common import *

DEBUG = True

SECRET_KEY = "django-insecure-up-or@dgm5uinvtiz8f(zlgd#inka*!1%=k1a!3w+%+#4a%ml+"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "laleh_store2",
        "HOST": "localhost",
        "USER": "root",
        "PASSWORD": "seyyedamirreza1381"
    }
}
