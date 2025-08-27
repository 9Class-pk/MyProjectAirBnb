from .models import City, Property, Service
from modeltranslation.translator import TranslationOptions,register

@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)


@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description',)


@register(Service)
class ProductTranslationOptions(TranslationOptions):
    fields = ('service_name',)
