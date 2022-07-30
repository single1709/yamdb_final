import uuid

from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdminOrReadOnly, IsAdminUser
from .serializers import RegisterSerializer, TokenSerializer, UserSerializer


class RegisterUser(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = uuid.uuid4()
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user, create = User.objects.get_or_create(
            username=username,
            email=email,
        )
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Ваш код подтверждения',
            f'Ваш код подтверждения: {confirmation_code}',
            'DEFAULT_FROM_EMAIL',
            [email],
            fail_silently=True,
        )
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK,
        )


class TokenCheck(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        if username and not User.objects.filter(username=username).exists():
            return Response(
                'Пользователь не найден',
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.data.get('username'))
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'token': str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, IsAdminOrReadOnly)
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                email=user.email,
                role=user.role,
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
