from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from survivers.models import Surviver
from survivers.serializers import SurviverSerializer
from rest_framework.response import Response

ITEMS = {'water': 4 , 'food': 3 , 'medications': 2 , 'ammunition': 1 }

@api_view(['POST'])
def survivers_create(request):
    """
    create a new surviver.
    """
    if request.method == 'POST':
        serializer = SurviverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survivers_list(request):
    """
    list all survivers.
    """
    if request.method == 'GET':
        survivers = Surviver.objects.all()
        serializer = SurviverSerializer(survivers, many=True)
        return Response(serializer.data)

@api_view(['GET', 'PUT'])
def surviver_update_location(request, pk):
    """
    Update location from surviver.
    """
    try:
        survivers = Surviver.objects.get(pk=pk)
    except Surviver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        survivers = SurviverSerializer(survivers)
        return Response(survivers.data)

    elif request.method == 'PUT':
        serializer = SurviverSerializer(survivers, data=request.data, partial=True)
        for value in request.data.keys():
            print(value)
            if value != "latitude" and value != "longitude":
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def relate_infected(request, pk):
    """
    Relate infected surviver
    """

    pass



