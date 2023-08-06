import traceback
from django.contrib.postgres.fields import DateTimeRangeField

from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from ievv_opensource.ievv_restframework_helpers.serializer_fields import DateTimeRangeSerializerField
from ievv_opensource.utils.validation_error_util import ValidationErrorUtil


class FullCleanModelSerializer(serializers.ModelSerializer):
    """
    A ``rest_framework.serializers.ModelSerializer`` subclass
    that calls full_clean() on the model instance before saving.
    """
    def clean_model_instance(self, instance):
        """
        Clean the model instance (full_clean()) and ensures any
        ``django.core.exceptions.ValidationError`` raised is re-raised as a
        ``rest_framework.exceptions.ValidationError``.
        """
        try:
            instance.full_clean()
        except ValidationError as e:
            raise ValidationErrorUtil(e).as_drf_validation_error()

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:

            return ExampleModel.objects.create(**validated_data)

        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:

            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance

        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        instance = ModelClass(**validated_data)
        self.clean_model_instance(instance)
        try:
            instance.save()
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.save()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)

        self.clean_model_instance(instance)
        instance.save()
        return instance


class IevvModelSerializer(FullCleanModelSerializer):
    def build_field(self, field_name, info, model_class, nested_depth):
        result = super().build_field(field_name, info, model_class, nested_depth)
        if isinstance(model_class._meta.get_field(field_name), DateTimeRangeField):
            return DateTimeRangeSerializerField, result[1]
        return result
