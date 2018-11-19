from django.test import TestCase
from django.test import Client
from datetime import datetime
from .models import County, Review, User, Picture, Crime
import json

class CountyInformationTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        county = County.objects.create(name="Jefferson", state="KY", population=10)
        user = User.objects.create(username="Angad", age=10, gender="F")
        Picture.objects.create(
            file_url="https://url.com",
            county=county,
            user=user,
            timestamp=datetime.now()
        )
        Crime.objects.create(
            county=county,
            type="violent",
            count=100
        )
        Crime.objects.create(
            county=county,
            type="not bad",
            count=20
        )


    def test_get_county_info(self):
        response = self.client.get('/county/1/')
        info = response.json()

        assert info["name"] == "Jefferson"
        assert info["state"] == "KY"
        assert info["population"] == 10
        assert len(info["image_urls"]) == 1
        assert info["image_urls"][0] == "https://url.com"


class GetCountyReviewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        county = County.objects.create(name="Jefferson", state="KY", population=10)
        user = User.objects.create(username="Angad", age=10, gender="F")
        Review.objects.create(
            description="This place was great",
            county=county,
            user=user,
            rating=8.5,
            timestamp=datetime.now()
        )
        Review.objects.create(
            description="This place was not so great",
            county=county,
            user=user,
            rating=2.5,
            timestamp=datetime.now()
        )

    def test_get_county_reviews(self):
        response = self.client.get('/review/all/1/')
        reviews = response.json()["reviews"]

        assert len(reviews) == 2
        assert reviews[0]["rating"] == 8.5
        assert reviews[1]["rating"] == 2.5


class ReviewCreateTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.county = County.objects.create(name="Jefferson", state="KY", population=10)
        self.user = User.objects.create(username="Angad", age=10, gender="F")

    def test_review_create(self):
        data = {
            "description": "This place was great",
            "rating": 8,
        }

        self.client.post('/review/create/1/', data=json.dumps(data), content_type='application/json')
        response = self.client.get('/review/all/1/')
        assert len(response.json()["reviews"]) == 1

    
class ReviewEditTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.county = County.objects.create(name="Jefferson", state="KY", population=10)
        self.user = User.objects.create(username="Angad", age=10, gender="F")
        self.review = Review.objects.create(
            description="This place was great",
            county=self.county,
            user=self.user,
            rating=8,
            timestamp=datetime.now()
        )

    def test_review_edit(self):
        data = {
            "description": "This place was awful",
            "rating": 4,
        }
        response = self.client.get('/review/all/1/')
        review = response.json()["reviews"][0]
        assert review["rating"] == 8
        assert review["description"] == "This place was great"

        self.client.post('/review/edit/1/', data=json.dumps(data), content_type='application/json')

        response = self.client.get('/review/all/1/')
        review = response.json()["reviews"][0]
        assert review["rating"] == 4
        assert review["description"] == "This place was awful"


class ReviewDeleteTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.county = County.objects.create(name="Jefferson", state="KY", population=10)
        self.user = User.objects.create(username="Angad", age=10, gender="F")
        self.review = Review.objects.create(
            description="This place was great",
            county=self.county,
            user=self.user,
            rating=8,
            timestamp=datetime.now()
        )

    def test_review_delete(self):
        response = self.client.get('/review/all/1/')
        reviews = response.json()["reviews"]
        assert len(reviews) == 1

        self.client.delete('/review/delete/1/')

        response = self.client.get('/review/all/1/')
        reviews = response.json()["reviews"]
        assert len(reviews) == 0
