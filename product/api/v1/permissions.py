from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Subscription


def make_payment(request):
    # TODO
    pass


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):

        user = request.user

        if user.is_authenticated:

            if user.is_student:
                course_id = view.kwargs.get('course_id')
                if course_id is not None:
                    return Subscription.objects.filter(user=user, course_id=course_id, is_active=True).exists()

            return user.is_stuff

        return False

    def has_object_permission(self, request, view, obj):
        # TODO
        pass


class ReadOnlyOrIsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
