from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from survivers.models import Surviver
from survivers.serializers import SurviverSerializer
from rest_framework.response import Response
from django.db.models import Sum

ITEMS_VALUES = {'water': 4 , 'food': 3 , 'medication': 2 , 'ammunition': 1 }

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
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def surviver_update_location(request, pk):
    """
    Update location from surviver.
    """
    try:
        survivers = Surviver.objects.get(pk=pk)
    except Surviver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = SurviverSerializer(survivers, data=request.data, partial=True)
        for value in request.data.keys():
            if value != "latitude" and value != "longitude":
                return Response(status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def relate_infected(request, pk):
    """
    relate infected surviver.
    """
    try:
        survivers = Surviver.objects.get(pk=pk)
    except Surviver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT' and len(request.data.keys()) == 1:
        if "infected" in request.data.keys():
            data = {"infected": survivers.infected + 1}
            serializer = SurviverSerializer(survivers, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

def percentage_infected_survivors():
    """
    relate percentage of infected surviver.
    """

    survivers = Surviver.objects.all()
    per_inf, per_no_inf = calc_mean_infected(survivers)
    return {'infected': per_inf, 'no_infected': per_no_inf}
    #return Response(serializer.data)

def mean_surviver_resources():
    """
    relate mean of survivor resources.

    """
    survivers = Surviver.objects.all()
    food, water, medication, ammunition = calc_mean_surviver_resources(survivers)
    #return Response(serializer.data)
    return {'food': food, 'water': water, 'medication': medication, 'ammunition': ammunition}

def lost_points():
    """
    Points lost because of infected survivor.

    """
    items = Surviver.objects.filter(infected__gte=(3)).aggregate(
        Sum('food'), Sum('water'), Sum('medication'), Sum('ammunition'))
    total_points = calc_lost_points(items)
    return {'total_points': total_points}

    #return Response(serializer.data)

@api_view(['GET'])
def show_reports(request):
    if request.method == 'GET':
        mean_infected = percentage_infected_survivors()
        mean_resources = mean_surviver_resources()
        total_points_lost = lost_points()
        data = dict(mean_infected, **mean_resources, **total_points_lost)

    return Response({'report': data}, status=status.HTTP_200_OK)

def calc_mean_infected(survivers):
    number_survivers = len(survivers)
    infected = [surviver for surviver in survivers if surviver.infected >= 3 ]
    number_inf = len(infected)
    percentage_inf = number_inf * 100 / number_survivers
    percentage_no_inf = 100 - percentage_inf
    return (percentage_inf, percentage_no_inf)

def calc_mean_surviver_resources(survivers):
    number_survivers = len(survivers)
    items = Surviver.objects.aggregate(Sum('food'), Sum('water'), Sum('medication'), Sum('ammunition'))
    food_media = items['food__sum'] / number_survivers
    water_media = items['water__sum'] / number_survivers
    medication_media = items['medication__sum'] / number_survivers
    ammunition_media = items['ammunition__sum'] / number_survivers
    return(food_media, water_media, medication_media, ammunition_media)

def calc_lost_points(items):
    points_water = items['water__sum'] * ITEMS_VALUES['water']
    points_food = items['food__sum'] * ITEMS_VALUES['food']
    points_medication = items['medication__sum'] * ITEMS_VALUES['medication']
    points_ammunition = items['ammunition__sum'] * ITEMS_VALUES['ammunition']
    total_points = points_food + points_water + points_medication + points_ammunition
    return total_points