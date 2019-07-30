from django.db import models
from django.db.models import F, Q
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class Programme (models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code


class Group (models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    year = models.CharField(max_length=3, choices=(('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV')))
    group_size = models.IntegerField()

    class Meta:
        ordering = ['-group_size']

    def __str__(self):
        return self.programme.code +" "+ str(self.year) +f" (Group size: {self.group_size})"


class Room (models.Model):
    name = models.CharField(max_length=10)
    size = models.FloatField()
    is_forced_power_status = models.BooleanField(default=False)
    power_state = models.BooleanField(default=False)

    class Meta:
        ordering = ['-size']

    def __str__(self):
        return self.name +f" (Room size: {self.size})"


class DayOfTheWeek (models.Model):
    abbr = models.CharField(max_length=10)

    def __str__(self):
        return self.abbr


class RoomAllocation (models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['group']

    def __str__(self):
        try:
            return self.group.programme.code+ " " +str(self.group.year)+f" (Group size: {self.group.group_size})" + " -> " +self.room.name +f" (Room size: {self.room.size})"
        except Exception:
            return self.group.programme.code+ " " +str(self.group.year)+f" (Group size: {self.group.group_size})"+ " -> " +"Unallocated"


class Lecture (models.Model):
    name = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    day = models.ForeignKey(DayOfTheWeek, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


def post_save_group(sender, instance, *args, **kwargs):
    print("In post save")
    if instance:
        print("In post save, create")
        lecture_objs = []
        room_allocations = RoomAllocation.objects.all()
        for lecture in Lecture.objects.all():
            lecture_objs.append(lecture)
        print(lecture_objs)
        if len(room_allocations) > 0:
            for i in range(len(room_allocations)):
                RoomAllocation.objects.first().delete()

        groups_desc = Group.objects.order_by(F('group_size').desc())
        room_desc = Room.objects.order_by(F('size').desc())

        print(groups_desc[0], room_desc[0])

        for i in range(len(Group.objects.all())):
            try:
                RoomAllocation(room=room_desc[i], group=groups_desc[i]).save()
            except Exception:
                RoomAllocation(room=None, group=groups_desc[i]).save()

post_delete.connect(post_save_group, sender=Group)
post_delete.connect(post_save_group, sender=Room)
post_save.connect(post_save_group, sender=Group)
post_save.connect(post_save_group, sender=Room)
