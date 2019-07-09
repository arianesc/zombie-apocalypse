from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from survivers.models import Surviver
from survivers.serializers import SurviverSerializer
from rest_framework.response import Response
from django.db.models import Sum

"""Points for items """
ITEMS_VALUES = {'water': 4 , 'food': 3 , 'medication': 2 , 'ammunition': 1 }

@api_view(['POST'])
def survivers_create(request):

    """ Create a new surviver """

    if request.method == 'POST':
        serializer = SurviverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def survivers_list(request):

    """ List all survivers """

    if request.method == 'GET':
        survivers = Surviver.objects.all()
        serializer = SurviverSerializer(survivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
def surviver_update_location(request, pk):

    """ Update location from surviver """

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

    """ relate infected surviver """

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


def calc_mean_infected(survivers):

    """ Function to calc mean infected """

    number_survivers = len(survivers)
    infected = [surviver for surviver in survivers if surviver.infected >= 3 ]
    number_inf = len(infected)
    percentage_inf = number_inf * 100 / number_survivers
    percentage_no_inf = 100 - percentage_inf
    return (percentage_inf, percentage_no_inf)

def percentage_infected_survivors():

    """ Relate percentage of infected surviver """

    survivers = Surviver.objects.all()
    per_inf, per_no_inf = calc_mean_infected(survivers)
    return {'infected_survivers': per_inf, 'no_infected_survivers': per_no_inf}

def calc_mean_surviver_resources(survivers):

    """ Function to calc mean surviver resources """

    number_survivers = len(survivers)
    items = Surviver.objects.aggregate(Sum('food'), Sum('water'), Sum('medication'), Sum('ammunition'))
    food_media = items['food__sum'] / number_survivers
    water_media = items['water__sum'] / number_survivers
    medication_media = items['medication__sum'] / number_survivers
    ammunition_media = items['ammunition__sum'] / number_survivers
    return(food_media, water_media, medication_media, ammunition_media)

def mean_surviver_resources():

    """ Relate mean of survivor resources """

    survivers = Surviver.objects.all()
    food, water, medication, ammunition = calc_mean_surviver_resources(survivers)
    return {'food_for_surviver': food, 'water_for_surviver': water,
                                            'medication_for_surviver': medication, 'ammunition_for_surviver': ammunition}

def calc_lost_points(items):

    """ Function to calc lost points because infected survivers """

    points_water = items['water__sum'] * ITEMS_VALUES['water']
    points_food = items['food__sum'] * ITEMS_VALUES['food']
    points_medication = items['medication__sum'] * ITEMS_VALUES['medication']
    points_ammunition = items['ammunition__sum'] * ITEMS_VALUES['ammunition']
    total_points = points_food + points_water + points_medication + points_ammunition
    return total_points

def lost_points():

    """ Points lost because of infected survivor """

    items = Surviver.objects.filter(infected__gte=(3)).aggregate(
        Sum('food'), Sum('water'), Sum('medication'), Sum('ammunition'))
    total_points = calc_lost_points(items)
    return {'total_points_lost': total_points}

@api_view(['GET'])
def show_reports(request):

    """ Show all resports """

    if request.method == 'GET':
        mean_infected = percentage_infected_survivors()
        mean_resources = mean_surviver_resources()
        total_points_lost = lost_points()
        data = dict(mean_infected, **mean_resources, **total_points_lost)

    return Response({'report': data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def trades_item_surviver(request, pk1, pk2):

    """ Method to trades item """

    if request.method == 'PUT':
        try:
            surviver1 = Surviver.objects.get(pk=pk1)
            surviver2 = Surviver.objects.get(pk=pk2)

        except Surviver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        """ Create variables to save trade items """

        food1 = int(request.GET.get('food1', '0'))
        water1 = int(request.GET.get('water1', '0'))
        medication1 = int(request.GET.get('medication1', '0'))
        ammunition1 = int(request.GET.get('ammunition1', '0'))

        food2 = int(request.GET.get('food2', '0'))
        water2 = int(request.GET.get('water2', '0'))
        medication2 = int(request.GET.get('medication2', '0'))
        ammunition2 = int(request.GET.get('ammunition2', '0'))

        """ Sum items to compare points"""

        sum1 = food1 * ITEMS_VALUES['food'] + water1 * ITEMS_VALUES['water']\
                + medication1 * ITEMS_VALUES['medication'] +  ammunition1 * ITEMS_VALUES['ammunition']

        sum2 = food2 * ITEMS_VALUES['food'] + water2 * ITEMS_VALUES['water']\
                + medication2 * ITEMS_VALUES['medication'] +  ammunition2 * ITEMS_VALUES['ammunition']

        """ Comparing points and making trade """

        if sum1 == sum2:
            data1 = {"food":food2 + surviver1.food - food1,
                    "water":water2 + surviver1.water - water1,
                    "medication":medication2 + surviver1.medication - medication1,
                    "ammunition":ammunition2 + surviver1.ammunition - ammunition1}
            data2 = {"food":food1 + surviver2.food - food2,
                    "water":water1 + surviver2.water - water2,
                    "medication":medication1 + surviver2.medication - medication2,
                    "ammunition":ammunition1 + surviver2.ammunition - ammunition2}

            serializer1 = SurviverSerializer(surviver1, data=data1, partial=True)
            serializer2 = SurviverSerializer(surviver2, data=data2, partial=True)

        if serializer1.is_valid() and serializer2.is_valid():
            serializer1.save()
            serializer2.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_400_BAD_REQUEST)
