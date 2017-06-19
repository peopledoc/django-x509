try:
    from django.db.models import UUIDField  # noqa F401
except ImportError:
    # Django < 1.8
    try:
        from uuidfield import UUIDField  # noqa F401
    except ImportError:
        raise ImportError("In order to use django-x509 with Django < 1.8 you "
                          "must install django-uuidfield.")
