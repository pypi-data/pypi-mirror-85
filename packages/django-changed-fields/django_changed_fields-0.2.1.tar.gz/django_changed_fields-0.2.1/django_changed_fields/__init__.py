"""
Mixin to show changed fields per DRF resource.
"""
from django.forms import model_to_dict


class ChangedFieldsMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_queryset = None

    def last_queryset(self):
        if not self.__last_queryset:
            self.__last_queryset = type(self).objects.get(pk=self.pk) if self.pk else None
        return self.__last_queryset

    def change_fields(self, *args, **kwargs):
        available_fields = map(
            lambda field: field.name,
            filter(
                lambda field: not isinstance(field, (ManyToManyField, ManyToOneRel)),
                self._meta.get_fields()
            )
        )
        new = set(filter(
            lambda item: item[0] in available_fields,
            model_to_dict(self, *args, **kwargs).items())
        )
        if not self.pk:
            return list(dict(new).keys())

        old = set(filter(
            lambda item: item[0] in available_fields,
            model_to_dict(self.last_queryset(), *args, **kwargs).items()
        ))
        return list(dict(new - old).keys())

    def save(self, *args, **kwargs):
        self.last_queryset()
        super().save(*args, **kwargs)
