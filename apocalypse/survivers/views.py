from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from survivers.models import Surviver
from survivers.serializers import SurviverSerializer

@csrf_exempt
def survivers_list(request):
    """
    List all code survivers, or create a new surviver.
    """
    if request.method == 'GET':
        survivers = Surviver.objects.all()
        serializer = SurviverSerializer(survivers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SurviverSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def surviver_detail(request, pk):
    """
    Retrieve, update or delete a code surviver.
    """
    try:
        survivers = Surviver.objects.get(pk=pk)
    except Surviver.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        survivers = SurviverSerializer(survivers)
        return JsonResponse(survivers.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SurviverSerializer(survivers, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        survivers.delete()
        return HttpResponse(status=204)