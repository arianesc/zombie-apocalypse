from django.test import TestCase
from survivers.models import Surviver
from django.db import IntegrityError
from rest_framework.test import APIClient
from survivers.views import calc_mean_infected\
                            ,calc_mean_surviver_resources\
                            ,calc_lost_points\
                            ,surviver_update_location
from django.db.models import Sum

ITEMS_VALUES = {'water': 4 , 'food': 3 , 'medication': 2 , 'ammunition': 1 }

class ModelTest(TestCase):

    def test_create_surviver(self):
        """ Test create a new surviver"""
        name = "Ana"
        age = 19
        gender = "female"
        latitude = "1871817"
        longitude = "88888"
        food = 2
        water = 9
        medication = 8
        ammunition = 4
        surviver = Surviver(
            name = name,
            age = age,
            gender = gender,
            latitude = latitude,
            longitude = longitude,
            food = food,
            water = water,
            medication = medication,
            ammunition = ammunition,
        )
        surviver.save()
        surviver_db = Surviver.objects.all().first()
        self.assertEquals(surviver,  surviver_db)

    def test_create_wrong_surviver(self):
        """ Test create a wrong surviver because missing obrigatory fields"""
        name = "Maria"
        age = 14
        surviver = Surviver(name=name)
        with self.assertRaises(Exception) as raised:
            surviver.save()
        self.assertEqual(IntegrityError, type(raised.exception))

class ReportTest(TestCase):

    def setUp(self):
        name = "Ana"
        age = 19
        gender = "female"
        latitude = "1871817"
        longitude = "88888"
        food = 2
        water = 9
        medication = 8
        ammunition = 4
        infected = 0
        surviver = Surviver(
            name = name,
            age = age,
            gender = gender,
            latitude = latitude,
            longitude = longitude,
            food = food,
            water = water,
            medication = medication,
            ammunition = ammunition,
            infected = infected,
        )
        surviver.save()
        name = "Ana"
        age = 19
        gender = "female"
        latitude = "1871817"
        longitude = "88888"
        food = 2
        water = 9
        medication = 8
        ammunition = 4
        infected = 3
        surviver2 = Surviver(
            name = name,
            age = age,
            gender = gender,
            latitude = latitude,
            longitude = longitude,
            food = food,
            water = water,
            medication = medication,
            ammunition = ammunition,
            infected = infected,
        )
        surviver2.save()

    def test_mean_infected(self):
        """ Test method that calculate the mean of infected survivers """
        surviver = Surviver.objects.all()
        infected, not_infected = calc_mean_infected(surviver)
        self.assertEqual(infected, 50.0)
        self.assertEqual(not_infected, 50.0)

    def test_mean_surviver_resources(self):
        """ Test method that calculate the mean of resources from survivers"""
        survivers = Surviver.objects.all()
        food, water, medication, ammunition = calc_mean_surviver_resources(survivers)

        self.assertEqual(food, 2)
        self.assertEqual(water, 9)
        self.assertEqual(medication, 8)
        self.assertEqual(ammunition, 4)

    def test_calc_lost_points(self):
        """ Test the method that calculate the lost points for infected survivers """
        items = Surviver.objects.filter(infected__gte=(3)).aggregate(
            Sum('food'), Sum('water'), Sum('medication'), Sum('ammunition'))

        lost_points = calc_lost_points(items)
        self.assertEqual(lost_points, 62)

class LocationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        name = "Ana"
        age = 19
        gender = "female"
        latitude = "1871817"
        longitude = "88888"
        food = 2
        water = 9
        medication = 8
        ammunition = 4
        infected = 0
        surviver = Surviver(
            name = name,
            age = age,
            gender = gender,
            latitude = latitude,
            longitude = longitude,
            food = food,
            water = water,
            medication = medication,
            ammunition = ammunition,
            infected = infected,
        )
        surviver.save()

    def test_surviver_update_location(self):

        latitude = "212"
        longitude = "111"
        response = self.client.put('/api/survivers/update_location/1/', {'longitude': longitude, 'latitude':latitude})
        self.assertEqual(response.status_code, 200)

    def test_surviver_update_location_wrong(self):

        latitude = "212"
        longitude = "111"
        name = "Maria"
        response = self.client.put('/api/survivers/update_location/1/', {'longitude': longitude, 'latitude':latitude, 'name':name})
        self.assertEqual(response.status_code, 400)