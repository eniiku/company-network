from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Company
from .serializers import CompanySerializer

class CompanyViewSet(viewsets.ViewSet):
    def get_queryset(self):
        return Company.nodes.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = Company(**serializer.validated_data).save()
            return Response(CompanySerializer(company).data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            company = serializer.save()
            return Response(CompanySerializer(company).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        company.delete()
        return Response(status=204)

    @action(detail=True, methods=['post'])
    def add_relationship(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        related_company_name = request.data.get('related_company_name')
        relationship_type = request.data.get('relationship_type')

        if not related_company_name or not relationship_type:
            return Response({'error': 'Missing related_company_name or relationship_type'},
status=400)

        try:
            related_company = Company.nodes.get(name=related_company_name)
        except Company.DoesNotExist:
            return Response({'error': 'Related company not found'}, status=404)

        if relationship_type == 'SUPPLIES':
            company.suppliers.connect(related_company)
        elif relationship_type == 'PARTNERS_WITH':
            company.partners.connect(related_company)
        elif relationship_type == 'COMPETES_WITH':
            company.competitors.connect(related_company)
        else:
            return Response({'error': 'Invalid relationship type'}, status=400)

        return Response({'success': 'Relationship added'}, status=201)

    @action(detail=True, methods=['get'])
    def get_relationships(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        relationships = {
            'suppliers': [{'name': c.name} for c in company.suppliers.all()],
            'customers': [{'name': c.name} for c in company.customers.all()],
            'partners': [{'name': c.name} for c in company.partners.all()],
            'competitors': [{'name': c.name} for c in company.competitors.all()],
        }
        return Response(relationships)