from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import GuideForm
from .serializers import GuideSerializer,HeroSerializer,ItemSerializer,RoleSerializer
from .models import Hero, Guide, Role, Item
import json
import requests
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken

def all_heroes(request):
    response = requests.get('https://api.opendota.com/api/heroes')
    heroes = response.json()
    serialized_heroes = HeroSerializer(heroes).all_heroes
    return JsonResponse(data=serialized_heroes, status=200)


def view_hero(request, hero_id):
    response = requests.get('https://api.opendota.com/api/heroes')
    heroes = response.json()
    hero = {}
    for i in range(len(heroes)):
        if hero_id == heroes[i]['id']:
            print(i)
            hero = heroes[i]
    serialized_hero = HeroSerializer(hero).hero_detail
    return JsonResponse(data=serialized_hero, status = 200)


def all_guides(request,hero_id):
    guides = Guide.objects.filter(hero=hero_id)
    serialized_guides = GuideSerializer(guides).all_guides
    return JsonResponse(data=serialized_guides, status = 200)


def view_guide(request,hero_id, guide_id):
    guides = Guide.objects.filter(hero=hero_id)
    serialized_guides = GuideSerializer(guides).all_guides
    return JsonResponse(data=serialized_guides, status = 200)


@csrf_exempt
def add_guide(request, hero_id):
    print(request)
    data = json.load(request)
    if request.method == "POST":
        form = GuideForm(data)
        if form.is_valid():
            guide = form.save(commit=True)
            serialized_guide = GuideSerializer(guide).guide_detail
            return JsonResponse(data=serialized_guide, status=200)
        else:
            return JsonResponse(data={'error': 'guide not created'}, status=500)

@csrf_exempt
def edit_guide(request,hero_id, guide_id):
    guides = Guide.objects.filter(hero = hero_id)
    guide = guides[guide_id]
    data = json.load(request)
    print(data)
    if request.method == "POST":
        form = GuideForm(data, instance=guide)
        if form.is_valid():
            guide = form.save(commit=True)
            serialized_guide = GuideSerializer(guide).guide_detail
            return JsonResponse(data=serialized_guide, status=200)


@csrf_exempt
def delete_guide(request,hero_id, guide_id):
    if request.method == "POST":
        guides = Guide.objects.filter(hero = hero_id)
        guide = guides[guide_id]
        guide.delete()
    return JsonResponse(data={'status': 'Successfully deleted guide.'}, status=200)

def all_roles(request):
    roles = Role.objects.all()
    serialized_roles = RoleSerializer(roles).all_roles
    return JsonResponse(data=serialized_roles, status = 200)


def view_role(request, role_id):
    role = Role.objects.get(id = role_id)
    serialized_role = RoleSerializer(role).role_detail
    return JsonResponse(data=serialized_role, status = 200)

def all_items(request):
    items = Item.objects.all()
    serialized_items = ItemSerializer(items).all_items
    return JsonResponse(data=serialized_items, status = 200)


def view_item(request, item_id):
    item = Item.objects.get(id = item_id)
    serialized_item = ItemSerializer(item).item_detail
    return JsonResponse(data=serialized_item, status = 200)

@api_view(['GET'])
def current_user(request):
    
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)