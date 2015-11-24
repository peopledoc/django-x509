try:
    from django.db.models import UUIDField
except ImportError:
    # Django < 1.8
    try:
        from uuidfield import UUIDField
    except ImportError:
        raise ImportError("In order to use django-x509 with Django < 1.8 you "
                          "must install django-uuidfield.")
    
