from django.urls import re_path
from room_monitor.api.views import (
    LectureNameListApiView,
    RoomNameListApiView,
    RoomPowerStatusListView,
    RoomPowerStatusUpdateView,
    GroupAddApiView,
    GroupListApiView,
    GroupDeleteApiView,
    GroupNameListApiView,
    GroupRetrieveApiView,
    GroupUpdateApiView,
    DayOfWeekAbbrListApiView,
    RoomAllocationListApiView,
    RoomTimetableListApiView,
    ProgrammeCodeListView,
    ArduinoRoomPowerStatusUpdateView,
    RoomPowerStatusRetrieveApiView,
)


app_name = 'room_monitor'
urlpatterns = [
    re_path(r'^day/list/$', DayOfWeekAbbrListApiView.as_view(), name='day-of-week'),
    re_path(r'^group/$', GroupListApiView.as_view(), name='group-list'),
    re_path(r'^group/add/$', GroupAddApiView.as_view(), name='add-group'),
    re_path(r'^group/(?P<pk>\d+)/delete/$', GroupDeleteApiView.as_view(), name='delete-group'),
    re_path(r'^group/(?P<pk>\d+)/$', GroupRetrieveApiView.as_view(), name='retrieve-group'),
    re_path(r'^group/(?P<pk>\d+)/update/$', GroupUpdateApiView.as_view(), name='update-group'),
    re_path(r'^lecture/name/$', LectureNameListApiView.as_view(), name='lecture-name'),
    re_path(r'^group/name/$', GroupNameListApiView.as_view(), name='group-name'),
    re_path(r'^programmes/$', ProgrammeCodeListView.as_view(), name='programmes'),
    re_path(r'^room/allocations/$', RoomAllocationListApiView.as_view(), name='room_allocation'),
    re_path(r'^room/name/$', RoomNameListApiView.as_view(), name='room-name'),
    re_path(r'^room/power_status/$', RoomPowerStatusListView.as_view(), name='room-power-status'),
    re_path(r'^room/power_status/(?P<room_name>\w+)/$', RoomPowerStatusRetrieveApiView.as_view(), name='room-power-status-retrieve'),
    re_path(r'^room/power_status/(?P<name>\w+)/update/$', RoomPowerStatusUpdateView.as_view(), name='room-power-status-update'),
    re_path(r'^room/power_status/arduino/(?P<pk>\d+)/(?P<power_status>\d+)/update/$', ArduinoRoomPowerStatusUpdateView.as_view(), name='arduino-room-power-status-update'),
    re_path(r'^timetable/(?P<room>\w+)/$', RoomTimetableListApiView.as_view(), name='room-time-table'),
]
