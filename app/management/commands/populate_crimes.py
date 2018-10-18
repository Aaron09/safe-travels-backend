from django.core.management.base import BaseCommand
from app.models import Crime, County
import pandas as pd

class Command(BaseCommand):

    def _populate_crimes(self):
        file_path = "data/crime_data_w_population_and_crime_rate.csv"
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            self._create_county(row)
            self._add_crime(row)


    def _create_county(self, row):
        county_name_info = [item.strip() for item in row["county_name"].split(",")]
        county_name, state = county_name_info[0], county_name_info[1]
        
        existing_county = len(County.objects.filter(name=county_name, state=state)) > 1

        if not existing_county:
            population = row["population"]
            county = County(name=county_name, state=state, population=population)
            county.save()
    

    def _add_crime(self, row):
        types = ["MURDER", "RAPE", "ROBBERY", "AGASSLT", "BURGLRY", "LARCENY", "MVTHEFT", "ARSON"]
        type_map = {
            "MURDER": "Murder",
            "RAPE": "Rape",
            "ROBBERY": "Robbery",
            "AGASSLT": "Aggravated Assault",
            "BURGLRY": "Burglary",
            "LARCENY": "Larceny",
            "MVTHEFT": "Motor Vehicle Theft",
            "ARSON": "Arson"
        }
        county_name_info = [item.strip() for item in row["county_name"].split(",")]
        county_name, state = county_name_info[0], county_name_info[1]
        county = County.objects.filter(name=county_name, state=state)[0]

        for type in types:
            type_name = type_map[type]
            crime = Crime(county_id=county, count=row[type], type=type_name)
            crime.save()


    def handle(self, *args, **options):
        self._populate_crimes()