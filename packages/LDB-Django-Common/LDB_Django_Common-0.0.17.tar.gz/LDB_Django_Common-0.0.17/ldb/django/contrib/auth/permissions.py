from django.contrib.auth import get_permission_codename


def get_permission_full_codename(model_cls, permission_action):
    """
    model_cls is the class of a model
    permission_action is the permission like {view, add, change, delete} (as a
        string)
    """
    permission_required_code = \
                get_permission_codename(permission_action, model_cls._meta)
    return f"{model_cls._meta.app_label}.{permission_required_code}"
