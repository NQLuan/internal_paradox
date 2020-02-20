from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Profile, Team, User
from api.serializers import MemberSerializer, TeamSerializers
from api.services import TeamService, TeamUtil
from api.views import BaseViewSet


class TeamViewSet(BaseViewSet):
    queryset = Team.objects.all()
    authentication_classes = (APIAuthentication,)
    serializer_class = TeamSerializers
    pagination_class = None
    permission_classes = (IsAdminUser,)
    permission_classes_by_action = {'list': [IsAuthenticated], 'retrieve': [IsAuthenticated]}

    """
    CREATE FUNCTION
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        TeamService.update_leader_teams(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    LIST FUNCTION
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        TeamService.list_team_member(serializer.data)
        return Response(serializer.data)

    """
    RETRIEVE FUNCTION
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        rs = TeamService.retrieve_team_member(serializer.data, instance)
        rs['non_members'] = TeamService.get_potential_members(instance)
        return Response(rs)

    """
    DELETE FUNCTION
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        TeamService.remove_team(instance)
        instance.delete()

    """
    GET EMPLOYEE THAT IS NOT LEADER FUNCTION
    """

    @action(methods=['get'], detail=False)
    def send_leader(self, request, *args, **kwargs):
        leaders = TeamService.get_leader()
        return Response(leaders)

    """
    ADD MEMBER TO TEAM FUNCTION
    """

    @action(methods=['put'], detail=True)
    def add_member(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        if data.get('emails'):
            for email in data.get('emails').split(','):
                data['email'] = email
                member_serializer = MemberSerializer(data=data)
                if member_serializer.is_valid(raise_exception=True):
                    validate_data = member_serializer.validated_data
                    if validate_data.get('email'):
                        TeamService.add_new_member(validate_data, instance)
        return Response({'Success': True})

    """
    REMOVE MEMBER FROM TEAM FUNCTION
    """

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
        instance = self.get_object()
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validate_data = serializer.validated_data
            user = User.objects.get(email=validate_data.get('email'))
            instance.team_leader = user.id
            instance.save()
        return Response({'Success': True})

    @action(methods=['get'], detail=True)
    def get_new_teams(self, request, *args, **kwargs):
        instance = Profile.objects.get(id=kwargs.get('pk'))
        queryset = Team.objects.exclude(id__in=instance.teams.split(','))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=False)
    def move_team(self, request, *args, **kwargs):
        user_id = int(request.data.get('user_id'))
        current_team_id = int(request.data.get('current_team_id'))
        new_team_id = int(request.data.get('new_team_id'))
        user_profile = Profile.objects.get(id=user_id)
        TeamUtil.remove_team(user_profile, current_team_id)
        user_profile.save()
        TeamUtil.update_teams(user_id, new_team_id)
        return Response({'Success': True})
