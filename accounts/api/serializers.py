from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer, EmailField, ValidationError,
    CharField, HyperlinkedIdentityField, SerializerMethodField
)

class UserLoginSerializer(ModelSerializer):
    token = CharField(read_only=True, allow_blank=True)
    username_or_email = CharField(allow_blank=True, required=False, label='Username or Email')

    class Meta:
        model = User
        fields = [
            'username_or_email',
            'password',
            'token'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email', None)
        password = attrs.get('password', None)
        if not username_or_email:
            raise ValidationError("Username/Email required ")

        user = User.objects.filter(
            Q(email=username_or_email) | Q(username=username_or_email)
        ).first()
        print(user)
        if user:
            user_obj = user
        else:
            raise ValidationError("Username/Email Invalid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Invalid password !")

        attrs['token'] = "Some TOken !"

        return attrs


