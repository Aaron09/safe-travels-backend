from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db import connection
from app.models import County, Review
from datetime import datetime
from textwrap import dedent
import json


def county_information(request, county_id):
    query = "select * from app_county where id={0}".format(county_id)
    result = County.objects.raw(query)
    serialized_result = serializers.serialize("json", result, fields=('name', 'state', 'population'))
    raw_county_data = json.loads(serialized_result)[0]
    return JsonResponse(raw_county_data["fields"])


def county_reviews(request, county_id):
    query = "select * from app_review where county_id={0}".format(county_id)
    result = Review.objects.raw(query)
    serialized_result = serializers.serialize(
        "json", result, fields=('description', 'county', 'user', 'rating', 'timestamp')
    )
    raw_review_data = json.loads(serialized_result)

    reviews = [raw_review["fields"] for raw_review in raw_review_data]
    return JsonResponse({"reviews": reviews})


def review_create(request, county_id):
    description = request.POST["description"]
    rating = request.POST["rating"]
    user = 1
    timestamp = datetime.now()

    query = "\
        insert into app_review (description, rating, user_id, county_id, timestamp) \
        values ('{0}', {1}, {2}, {3}, '{4}') \
    ".format(description, rating, user, county_id, timestamp)

    query = dedent(query)

    with connection.cursor() as cursor:
        result = cursor.execute(query)

    return HttpResponse(200)


def review_edit(request, review_id):
    description = request.POST["description"]
    rating = request.POST["rating"]
    user = 1
    timestamp = datetime.now()

    query = "\
        update app_review \
        set description='{0}', rating={1}, timestamp='{2}' \
        where id={3}\
    ".format(description, rating, timestamp, review_id)

    query = dedent(query)
    with connection.cursor() as cursor:
        result = cursor.execute(query)

    return HttpResponse(200)


def review_delete(request, review_id):
    query = "\
        delete from app_review \
        where id={0} \
    ".format(review_id)

    query = dedent(query)
    with connection.cursor() as cursor:
        result = cursor.execute(query)

    return HttpResponse(200)
