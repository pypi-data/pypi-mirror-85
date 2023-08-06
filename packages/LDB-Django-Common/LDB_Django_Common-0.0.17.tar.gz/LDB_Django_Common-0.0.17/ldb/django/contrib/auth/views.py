from ldb.django.contrib.auth.mixins import AuthorizedMixin

from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView)

#TODO: Test these
class AuthorizedListView(AuthorizedMixin, ListView): pass
class AuthorizedDetailView(AuthorizedMixin, DetailView): pass
class AuthorizedCreateView(AuthorizedMixin, CreateView): pass
class AuthorizedUpdateView(AuthorizedMixin, UpdateView): pass
class AuthorizedDeleteView(AuthorizedMixin, DeleteView): pass
