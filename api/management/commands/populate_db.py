from django.core.management.base import BaseCommand
from neomodel import db
from api.models import Company

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        db.cypher_query("MATCH (n) DETACH DELETE n")

        # Create companies
        companies = [
            Company(name='Apple', industry='Technology', founded_year='1976'),
            Company(name='Microsoft', industry='Technology', founded_year='1975'),
            Company(name='Amazon', industry='E-commerce', founded_year='1994'),
            Company(name='Google', industry='Technology', founded_year='1998'),
            Company(name='Facebook', industry='Social Media', founded_year='2004')
        ]
        for company in companies:
            company.save()

        # Create relationships
        relationships = [
            (companies[0], 'competitors', companies[1]),
            (companies[0], 'competitors', companies[3]),
            (companies[1], 'competitors', companies[3]),
            (companies[2], 'competitors', companies[3]),
            (companies[3], 'competitors', companies[4]),
            (companies[0], 'suppliers', companies[2]),
            (companies[1], 'suppliers', companies[2])
        ]
        for source, rel_type, target in relationships:
            getattr(source, rel_type).connect(target)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))