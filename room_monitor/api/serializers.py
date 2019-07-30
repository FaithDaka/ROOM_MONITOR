from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField
)
from django.contrib.auth.models import User
from room_monitor.models import Room, Group, Lecture, DayOfTheWeek, RoomAllocation, Programme


class RoomPowerStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'is_forced_power_status',
            'power_state'
        )


class RoomPowerStatusListSerializer(ModelSerializer):
    group = SerializerMethodField()
    room_status_update_url = HyperlinkedIdentityField(
        view_name='room-monitor-api:room-power-status-update',
        lookup_field='name'
    )

    class Meta:
        model = Room
        fields = (
            'room_status_update_url',
            'name',
            'power_state',
            'group'
        )

    def get_group(self, obj):
        room_id = obj.id
        group_allocated = RoomAllocation.objects.filter(room=room_id)
        if group_allocated:
            group = group_allocated.first().group
            return group.programme.code +" "+ str(group.year)
        else:
            return None


class GroupSerializer(ModelSerializer):
    programme_code = SerializerMethodField()
    group_detail_url = HyperlinkedIdentityField(
        view_name='room-monitor-api:update-group'
    )
    group_delete_url = HyperlinkedIdentityField(
        view_name='room-monitor-api:delete-group'
    )
    class Meta:
        model = Group
        fields = (
            'programme_code',
            'year',
            'group_size',
            'group_detail_url',
            'group_delete_url'
        )

    def get_programme_code(self, obj):
        return obj.programme.code


class GroupCreateSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'programme',
            'year',
            'group_size',
        )


class GroupNameSerializer(ModelSerializer):
    name = SerializerMethodField()
    class Meta:
        model = Group
        fields = (
            'name',
        )

    def get_name(self, obj):
        return obj.programme.code +" "+ str(obj.year)


class RoomNameSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = (
            'name',
        )


class LectureNameSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = (
            'name',
        )


class ProgrammeCodeSerializer(ModelSerializer):
    class Meta:
        model = Programme
        fields = (
            'code',
        )


class DayOfWeekAbbrSerializer(ModelSerializer):
    class Meta:
        model = DayOfTheWeek
        fields = ('abbr', )


class RoomAllocationSerializer(ModelSerializer):
    group_name = SerializerMethodField()
    room_name = SerializerMethodField()

    class Meta:
        model = RoomAllocation
        fields = (
            'group_name',
            'room_name'
        )

    def get_group_name(self, obj):
        return obj.group.programme.code +" "+ str(obj.group.year)

    def get_room_name(self, obj):
        try:
            return obj.room.name
        except Exception:
            return None


class TimetableSerializer(ModelSerializer):
    end_time = SerializerMethodField()
    class Meta:
        model = Lecture
        fields = (
            'start_time',
            'end_time',
        )

    def get_end_time(self, obj):
        return (obj.end_time - 1)


class ArduinoPowerStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = (
            'start_time',
            'end_time',
        )
