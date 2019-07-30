from django.contrib.admin import AdminSite
from room_monitor.models import (
    Group,
    Lecture,
    Programme,
    Room,
    DayOfTheWeek,
    RoomAllocation,
)
from django.contrib.auth.models import User, Group as Group_




class RoomMonitorAdminSite(AdminSite):
    site_header = "Room Monitor Administration"
    site_title = "Room Monitor Admin Portal"
    index_title = "Welcome to Room Monitor Portal"

room_monitor_admin_site = RoomMonitorAdminSite(name='event_admin')

room_monitor_admin_site.register(User)
room_monitor_admin_site.register(Group_)
room_monitor_admin_site.register(Group)
room_monitor_admin_site.register(Lecture)
room_monitor_admin_site.register(Programme)
room_monitor_admin_site.register(Room)
room_monitor_admin_site.register(DayOfTheWeek)
room_monitor_admin_site.register(RoomAllocation)
