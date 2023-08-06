class InitialKwargsMixin:
    """
    Use this by using .as_view(initial_kwargs={'form_key1': 'kwarg_key1',
                                               'form_key2': 'kwarg_key2'})
    """
    initial_kwargs = {}

    def get_initial(self):
        initials = super().get_initial()

        for form_key, kwargs_key in self.initial_kwargs.items():
            initials[form_key] = self.kwargs[kwargs_key]

        return initials
