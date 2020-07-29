from builtins import object
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User

class GuideSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_guides(self):
        output = {'guides': []}

        for guide in self.body:
            guide_details = {
                'guide_name': guide.guide_name,
                'guide_body': guide.guide_body,
                'hero': guide.hero,
                'published':guide.published
            }
            output['guides'].append(guide_details)

        return output

    @property
    def guide_detail(self):
        return {
            'guide_name': self.body.guide_name,
            'guide_body': self.body.guide_body,
            'hero': self.body.hero,
            'published':self.body.published
        }

class HeroSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_heroes(self):
        output = {'heroes': []}

        for hero in self.body:
            hero_details = {
                'id':hero['id'],
                'hero_name': hero['localized_name'],
                'attribute': hero['primary_attr'],
                'attack_type': hero['attack_type'],
                'roles':hero['roles']
            }
            output['heroes'].append(hero_details)

        return output


    @property
    def hero_detail(self):
        return {
            'id':self.body['id'],
            'hero_name': self.body['localized_name'],
            'attribute': self.body['primary_attr'],
            'attack_type': self.body['attack_type'],
            'roles':self.body['roles']
        }


class RoleSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_roles(self):
        output = {'roles': []}

        for role in self.body:
            role_details = {
                'role_name': role['role_name']
            }
            output['roles'].append(role_details)

        return output

    @property
    def role_detail(self):
        return {
            'role_name': self.body['role_name'],
        }

class ItemSerializer(object):
    def __init__(self, body):
        self.body = body

    @property
    def all_items(self):
        output = {'items': []}

        for item in self.body:
            item_details = {
                'item_name': item['item_name'],
                'item_description': item['item_description']
            }
            output['items'].append(item_details)

        return output

    @property
    def item_detail(self):
        return {
            'item_name': self.body['item_name'],
            'item_description': self.body['item_description']
        }

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password')