from django.contrib import admin
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin, TranslationBaseModelAdmin,TranslationTabularInline
from .models import City, UserProfile, Property, Review, Booking, PropertyImage, Service, Favorite, FavoriteItem

admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Favorite)
admin.site.register(FavoriteItem)



class BaseTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Service, City  )
class ProductAdmin(BaseTranslationAdmin):
    pass



class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0



@admin.register(Property)
class PropertyAdmin(BaseTranslationAdmin):
    list_display = ("title", "city", "owner", "max_guests", "bedrooms", "bathrooms", "is_active")
    list_filter = ("city",  "is_active")
    search_fields = ("title", "description", "address")
    inlines = [PropertyImageInline,]


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("property", "guest", "check_in", "check_out", "status", "created_at")
    list_filter = ("status", "check_in", "check_out")
    search_fields = ("property__title", "guest__username")









