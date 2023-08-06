from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.views.generic.edit import (BaseCreateView, BaseUpdateView,
                                       BaseDeleteView)
from django.contrib.auth import get_permission_codename

from ldb.django.contrib.auth.permissions import get_permission_full_codename

class OwnedObjectQuerysetMixin(LoginRequiredMixin):
    """
    CBV mixin which filters the queryset based on owner.

    Assumes that the model is an OwnedModel, or at least that it has an owner
    foreign key to the auth user.
    """
    def get_queryset(self):
        queryset = super(OwnedObjectQuerysetMixin, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnedObjectFormMixin(LoginRequiredMixin):
    """
    CBV mixin that adds the logged in user's instance to the created object.
    """
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnedObjectFormMixin, self).form_valid(form)


class AuthorizedMixin(PermissionRequiredMixin):
    """
    CBV mixin that makes views require either a permission based on their type.
    Default is view, BaseCreateView subclasses require add, BaseUpdateView
    subclasses require change and BaseDeleteView subclasses required delete.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # This appears to be an abstract version of some CBV
        # If this is a bad assumption, then something needs to be done about
        # cls.model._meta below
        if cls.model is None:
            return

        permission_action = 'view'

        if hasattr(cls, 'permission_action'):
            permission_action = cls.permission_action
        elif issubclass(cls, BaseCreateView):
            permission_action = 'add'
        elif issubclass(cls, BaseUpdateView):
            permission_action = 'change'
        elif issubclass(cls, BaseDeleteView):
            permission_action = 'delete'

        cls.permission_required = \
                get_permission_full_codename(cls.model, permission_action)
