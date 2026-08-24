from django.test import Client, TestCase
from django.template.context_processors import static
from django.db.models import Max

# Create your tests here.
from .models import Airport, Passenger, Flights

class FlightTestCase(TestCase):

    def setUp(self):

        a1=Airport.objects.create(code="AAA", city="City A")
        a2=Airport.objects.create(code="BBB", city="City B")

        Flights.objects.create(origin=a1 , destination=a2 , duration=100)
        Flights.objects.create(origin=a1 , destination=a1 , duration=200)
        Flights.objects.create(origin=a1 , destination=a2 , duration=-100)

    def test_departures_count(self):
            a=Airport.objects.get(code="AAA")
            self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
            a=Airport.objects.get(code="AAA")
            self.assertEqual(a.arrivals.count(), 1)

    def test_is_valid(self):
            a1=Airport.objects.get(code="AAA")
            a2=Airport.objects.get(code="BBB")
            f=Flights.objects.get(origin=a1,destination=a2, duration=100)
            self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
            a1=Airport.objects.get(code="AAA")
            f=Flights.objects.get(origin=a1,destination=a1)
            self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
            a1=Airport.objects.get(code="AAA")
            a2=Airport.objects.get(code="BBB")
            f=Flights.objects.get(origin=a1,destination=a2,duration=-100)
            self.assertFalse(f.is_valid_flight())

    def text_index(self):
           c=Client()
           response=c.get("/flight/")
           self.assertEqual(response.status_code, 200)
           self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
           a1=Airport.objects.get(code="AAA")
           f=Flights.objects.get(origin=a1,destination=a1)

           c=Client()

           response=c.get(f"/flight/{f.id}")
           self.assertEqual(response.status_code,200)

    def test_invalid_flight_page(self):
           max_id=Flights.objects.all().aggregate(Max("id"))["id__max"]

           c=Client()
           response=c.get(f"/flight/{max_id + 1}")
           self.assertEqual(response.status_code, 404)