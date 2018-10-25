from django.test import TestCase
from django.test import Client
from .models import County

class CountyInformationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        County.objects.create(name="Jefferson", state="KY", population=10)

    def test_get_county_info(self):
        response = self.client.get('/county/1/')
        info = response.json()
        
        assert info["name"] == "Jefferson"
        assert info["state"] == "KY"
        assert info["population"] == 10