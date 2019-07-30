from datetime import datetime
from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
)
from room_monitor.models import Room, Group, Lecture, Programme, DayOfTheWeek, RoomAllocation
from room_monitor.api.serializers import (
    GroupSerializer,
    GroupCreateSerializer,
    LectureNameSerializer,
    RoomNameSerializer,
    RoomPowerStatusListSerializer,
    GroupNameSerializer,
    DayOfWeekAbbrSerializer,
    RoomAllocationSerializer,
    TimetableSerializer,
    ProgrammeCodeSerializer,
    RoomPowerStatusUpdateSerializer
)


class RoomPowerStatusRetrieveApiView(RetrieveAPIView):
    serializer_class = RoomPowerStatusUpdateSerializer
    lookup_url_kwarg = "room_name"
    lookup_field = "name"

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        queryset = Room.objects.filter(name=room_name)
        return queryset


class RoomPowerStatusListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomPowerStatusListSerializer


class RoomPowerStatusUpdateView(RetrieveUpdateAPIView):
    serializer_class = RoomPowerStatusUpdateSerializer
    lookup_url_kwarg = "name"
    lookup_field = "name"

    def get_queryset(self):
        room_name = self.kwargs['name']
        queryset = Room.objects.filter(name=room_name)
        return queryset


class GroupListApiView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupAddApiView(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer


class GroupDeleteApiView(RetrieveDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupRetrieveApiView(RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupUpdateApiView(RetrieveUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer


class DayOfWeekAbbrListApiView(ListAPIView):
    queryset = DayOfTheWeek.objects.all()
    serializer_class = DayOfWeekAbbrSerializer


class LectureNameListApiView(ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureNameSerializer


class GroupNameListApiView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupNameSerializer


class RoomNameListApiView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomNameSerializer


class RoomAllocationListApiView(ListAPIView):
    queryset = RoomAllocation.objects.all()
    serializer_class = RoomAllocationSerializer


class RoomTimetableListApiView(ListAPIView):
    serializer_class = TimetableSerializer

    def get_queryset(self):
        try:
            room = Room.objects.filter(name=self.kwargs['room']).first()
            group = RoomAllocation.objects.filter(room=room.id).first().group
            today = datetime.today()
            weekday = today.strftime("%A")
            day = DayOfTheWeek.objects.filter(abbr=weekday).first()
            lectures = Lecture.objects.filter(day=day, group=group).order_by('start_time')
            return lectures
        except Exception:
            return []


class ProgrammeCodeListView(ListAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeCodeSerializer



class ArduinoRoomPowerStatusUpdateView(RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomPowerStatusListSerializer

    def perform_update(self, serializer):
        print("in perform_update")
        power_status = self.kwargs.get('power_status', None)
        print(power_status == str(1))
        if power_status == str(1):
            print("in power_status == 1")
            return serializer.save(power_status=True)
        else:
            print("in power_status == 0")
            return serializer.save(power_status=False)
