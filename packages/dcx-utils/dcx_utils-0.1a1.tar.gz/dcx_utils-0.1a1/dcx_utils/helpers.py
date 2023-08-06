from copy import deepcopy

from rest_framework import serializers
from rest_framework.metadata import SimpleMetadata
from rest_framework.reverse import reverse
from rest_framework.relations import Hyperlink


class DcxMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = super().determine_metadata(request, view)
        fields = self.get_serializer_info(view.get_serializer())
        metadata['schema'] = fields

        if hasattr(view, 'fields_choices'):
            field_choices = deepcopy(view.fields_choices)
            for field_name, choice_opt in field_choices.items():
                choice_opt['source'] = reverse(
                    f'{choice_opt["source"]}-list', request=request
                )
                fields[field_name]['choices'] = field_choices[
                    field_name]

        if hasattr(view, 'grouping'):
            metadata['grouping'] = view.grouping

        return metadata


class DcxModelSerializer(serializers.HyperlinkedModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if hasattr(self.Meta, 'related_fields'):
            related = self.Meta.related_fields

            for field in related:
                context_url = data['url'] + field + '/'
                field_data = {
                    'links': {
                        'context': context_url,
                        'rel': field,
                    }
                }

                if isinstance(data[field], Hyperlink):
                    field_data['links']['href'] = str(data[field])
                    field_data['display_value'] = str(getattr(instance, field))
                elif isinstance(data[field], list):
                    display_value = [f'{str(value)}' for value in getattr(instance, field).all()]
                    field_data['display_value'] = ', '.join(display_value)
                    field_data['links']['objects'] = [o for o in data[field]]

                data[field] = field_data

        data['display_value'] = str(instance)
        return data
