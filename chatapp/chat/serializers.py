from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import serializers
from chat.models import User, Topic, Farm, Forum

#User = get_user_model()
# User Serializer

class FarmSerializer(serializers.ModelSerializer):
    #topics = TopicSerializer(many=True, read_only=True)
    class Meta:
        model = Farm
        fields = [
            'pk',
            'name',
            'location',
            'image' 
        ]

class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password',) 

class TopicSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Topic
        fields = [
            'topic',
            'farm',
            'created_by',
            'timestamp',
        ]

    def validate_topic(self, value):
        qs = Topic.objects.filter(topic__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Topic alredy exist.")
        return value

# Message Serializer
class ForumSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    
    class Meta:
        model = Forum
        fields = ['topic', 'farm', 'message', 'message_by', 'timestamp']

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm
    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        ###### FILTER YOUR USER MODEL ######
        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            ###### USE YOUR TEXT FILE ######
            'email_template_name': 'example_message.txt',

            'request': request,
        }
        self.reset_form.save(**opts)

