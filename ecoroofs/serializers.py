from rest_framework import serializers


class ModelSerializer(serializers.ModelSerializer):

    def get_field_names(self, *args, **kwargs):
        names = super().get_field_names(*args, **kwargs)
        if 'url' not in names:
            names.append('url')
        return names

    def get_extra_kwargs(self, *args, **kwargs):
        extra_kwargs = super().get_extra_kwargs(*args, **kwargs)
        if 'url' not in extra_kwargs:
            view = self.context['view']
            lookup_field = view.lookup_field
            extra_kwargs['url'] = {'lookup_field': lookup_field}
        return extra_kwargs
