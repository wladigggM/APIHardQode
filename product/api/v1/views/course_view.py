from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription, Balance


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()

    def create(self, request, *args, **kwargs):
        """Метод создания урока"""

        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы """

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk=None):
        """Покупка доступа к курсу (подписка на курс)."""

        # TODO
        course = self.get_object()
        user = request.user

        try:
            balance = Balance.objects.get(user=user)
        except Balance.DoesNotExist:
            return Response({'details': "Balance not found"}, status=status.HTTP_404_NOT_FOUND)
        if Subscription.objects.filter(user=user, course=course, is_active=True).exists():
            return Response({"detail": "You already have an active subscription to this course."},
                            status=status.HTTP_400_BAD_REQUEST)
        price = course.price

        if balance.balance < price:
            return Response({"detail": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        balance.write_off(price)

        subscription = Subscription.objects.create(user=user, course=course, is_active=True)

        serializer = SubscriptionSerializer(subscription)
        data = serializer.data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def available(self, request):
        """Список доступных курсов"""

        # TODO
        user = request.user
        user_subs_ids = Subscription.objects.filter(user=user, is_active=True).values_list('course_id', flat=True)
        available_courses = Course.objects.exclude(id__in=user_subs_ids)

        serializer = CourseSerializer(available_courses, many=True)
        data = serializer.data

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        """Метод создания курса"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )