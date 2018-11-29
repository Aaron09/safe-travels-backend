from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db import connection
from app.models import County, Review, Picture
from datetime import datetime
from textwrap import dedent
from django.views.decorators.csrf import csrf_exempt
import boto3
import json
import random, string
import numpy as np
from app.models import County


def counties(request):
    query = "select * from app_county"
    result = County.objects.raw(query)
    serialized_result = serializers.serialize("json", result, fields=('name', 'state'))
    response = json.loads(serialized_result)

    return JsonResponse({ "counties": response })


def county_information(request, county_id):
    query = "select * from app_county where id={0}".format(county_id)
    result = County.objects.raw(query)
    serialized_result = serializers.serialize("json", result, fields=('name', 'state', 'population'))
    raw_county_data = json.loads(serialized_result)[0]

    response = raw_county_data["fields"]

    query = "select file_url from app_picture where county_id={0}".format(county_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        image_urls = [row[0] for row in cursor.fetchall()]

    response["image_urls"] = image_urls

    query = "select * from app_crime where county_id={0}".format(county_id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        crimes = [{"count": row[1], "type": row[2]} for row in cursor.fetchall()]

    response["crimes"] = crimes

    return JsonResponse(response)

def county_similar(request, county_id):
    county_id = int(county_id)
    query = "select * from app_county"
    with connection.cursor() as cursor:
        cursor.execute(query)
        counties = [{"id": row[0], "population": row[3], "name": row[1], "state": row[2]} for row in cursor.fetchall()]

    county_to_pop_dict = {}
    count_to_name_dict = {}
    for county in counties:
        county_to_pop_dict[county["id"]] = county["population"]
        count_to_name_dict[county["id"]] = county["name"]

    # Query all of the crimes
    query = "select * from app_crime"
    with connection.cursor() as cursor:
        cursor.execute(query)
        crimes = [{"county": row[3], "count": row[1], "type": row[2]} for row in cursor.fetchall()]

    county_to_crime_list_dict = {}
    crime_types = ["Murder", "Rape", "Robbery", "Aggravated Assault", "Burglary", "Larceny", "Motor Vehicle Theft", "Arson"]

    for crime in crimes:
        id = crime["county"]
        population = county_to_pop_dict[county_id]
        crime_type = crime["type"]
        crime_percentage = crime["count"] / population
        if id not in county_to_crime_list_dict:
            county_to_crime_list_dict[id] = np.zeros(len(crime_types))
        county_to_crime_list_dict[id][crime_types.index(crime_type)] = crime_percentage

    county_percentages = county_to_crime_list_dict[county_id]
    distance_list = []

    for key, val in county_to_crime_list_dict.items():
        distance = np.linalg.norm(county_percentages - val)
        distance_list.append((distance, key))

    sorted_values = sorted(distance_list, key=lambda a: a[0])[1:11]
    print(sorted_values)

    counties = [{"name": count_to_name_dict[item[1]], "county_id": item[1]} for item in sorted_values]
    return JsonResponse({"counties": counties})


def county_reviews(request, county_id):
    query = "select * from app_review where county_id={0}".format(county_id)
    result = Review.objects.raw(query)
    serialized_result = serializers.serialize(
        "json", result, fields=('description', 'county', 'user', 'rating', 'timestamp')
    )
    raw_review_data = json.loads(serialized_result)

    reviews = []
    for raw_review in raw_review_data:
        fields = raw_review["fields"]
        fields.update({'id': raw_review['pk']})
        reviews.append(fields)

    return JsonResponse({"reviews": reviews})

@csrf_exempt
def review_create(request, county_id):
    data = json.loads(request.body.decode('utf-8'))
    description = data["description"]
    rating = data["rating"]
    user = 2
    timestamp = datetime.now()

    query = "\
        insert into app_review (description, rating, user_id, county_id, timestamp) \
        values ('{0}', {1}, {2}, {3}, '{4}') \
    ".format(description, rating, user, county_id, timestamp)

    query = dedent(query)

    with connection.cursor() as cursor:
        result = cursor.execute(query)

    return HttpResponse(200)


@csrf_exempt
def review_edit(request, review_id):
    data = json.loads(request.body.decode('utf-8'))
    description = data["description"]
    rating = data["rating"]
    user = 2
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


@csrf_exempt
def review_delete(request, review_id):
    query = "\
        delete from app_review \
        where id={0} \
    ".format(review_id)

    query = dedent(query)
    with connection.cursor() as cursor:
        result = cursor.execute(query)

    return HttpResponse(200)


@csrf_exempt
def add_picture(request, county_id):
    img = request.FILES.get("image")

    remote_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

    s3 = boto3.resource('s3')
    s3.Bucket('safetravels-pictures').put_object(Key=remote_id, Body=img)

    remote_path = "https://s3.amazonaws.com/safetravels-pictures/" + remote_id

    Picture.objects.create(
        file_url=remote_path,
        county_id=county_id,
        user_id=2,
        timestamp=datetime.now()
    )

    return HttpResponse(200)
