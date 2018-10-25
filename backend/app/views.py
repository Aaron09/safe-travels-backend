from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from app.models import County
import json

def county_information(request, county_id):
    query = f"select * from app_county where id={county_id}"
    result = County.objects.raw(query)
    serialized_result = serializers.serialize("json", result, fields=('name', 'state', 'population'))
    raw_county_data = json.loads(serialized_result)[0]
    return JsonResponse(raw_county_data["fields"])