from rest_framework import permissions
from django.utils import timezone


class IsGuest(permissions.BasePermission):
    """
    Доступ только для аутентифицированных пользователей с ролью guest
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "guest"
        )


class IsHost(permissions.BasePermission):
    """
    Доступ для хостов.
    GET — доступен всем (чтение).
    POST/PUT/DELETE — только для хостов.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "host"
        )

    def has_object_permission(self, request, view, obj):
        # Хост может редактировать только свои объекты
        return obj.owner == request.user


class CanBookProperty(permissions.BasePermission):
    """
    Разрешает бронирование только гостям для активных объектов
    и только если даты свободны.
    """
    message = "Вы не можете забронировать это жильё."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "guest"
        )

    def has_object_permission(self, request, view, obj):
        if not obj.is_active:
            self.message = "Это жильё сейчас недоступно для бронирования."
            return False

        check_in = request.data.get("check_in")
        check_out = request.data.get("check_out")

        if not check_in or not check_out:
            self.message = "Не указаны даты бронирования."
            return False

        try:
            check_in_date = timezone.datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = timezone.datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            self.message = "Неверный формат даты. Используйте YYYY-MM-DD."
            return False

        if check_in_date >= check_out_date:
            self.message = "Дата выезда должна быть позже даты заезда."
            return False

        overlapping = obj.bookings.filter(
            status__in=["pending", "approved"],
            check_in__lt=check_out_date,
            check_out__gt=check_in_date,
        ).exists()

        if overlapping:
            self.message = "На выбранные даты жильё уже забронировано."
            return False

        return True


class HostBookingPermission(permissions.BasePermission):
    """
    Хост может изменять бронирования только своих объектов
    """
    message = "Вы можете управлять только бронированиями своих объектов."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, "role", None) == "host"
        )

    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user
