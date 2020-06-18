from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api_base.services import Utils
from api_base.views import BaseViewSet
from api_team.models import Team
from api_team.serializers import TeamSerializers, MemberSerializer
from api_team.services import TeamService
from api_user.models import Profile


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    authentication_classes = (APIAuthentication,)
    serializer_class = TeamSerializers
    pagination_class = None
    permission_classes = (IsAdminUser,)
    permission_classes_by_action = {'list': [IsAuthenticated], 'retrieve': [IsAuthenticated]}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        TeamService.delete_team(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def send_leader(self, request, *args, **kwargs):
        leaders = TeamService.get_leader()
        return Response(leaders)

    @action(methods=['put'], detail=True)
    def add_member(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        if data.get('emails'):
            for email in data.get('emails').split(','):
                data.update(email=email)
                member_serializer = MemberSerializer(data=data)
                if member_serializer.is_valid(raise_exception=True):
                    validate_data = member_serializer.validated_data
                    if validate_data.get('email'):
                        TeamService.add_new_member(instance, **validate_data)
        return Response({'Success': True})

    @action(methods=['put'], detail=True)
    def remove_member(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validate_data = serializer.validated_data
            TeamService.remove_member(validate_data, instance)
        return Response({'Success': True})

    @action(methods=['put'], detail=True)
    def set_leader(self, request, *args, **kwargs):
        team = self.get_object()
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validate_data = serializer.validated_data
            TeamService.set_leader(team, **validate_data)
            return Response({'Success': True})

    @action(methods=['get'], detail=True)
    def get_new_teams(self, request, *args, **kwargs):
        instance = Profile.objects.get(id=kwargs.get('pk'))
        queryset = Team.objects.exclude(id__in=instance.teams.split(','))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=False)
    def move_team(self, request, *args, **kwargs):
        user_id = Utils.convert_to_int(request.data.get('user_id'))
        current_team_id = Utils.convert_to_int(request.data.get('current_team_id'))
        new_team_id = Utils.convert_to_int(request.data.get('new_team_id'))
        TeamService.move_team(user_id, current_team_id, new_team_id)
        return Response({'Success': True})
