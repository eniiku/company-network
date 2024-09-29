from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Company
from .serializers import CompanySerializer

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return bool(
            request.method in ['GET', 'HEAD', 'OPTIONS'] or
            (is_authenticated and request.user and request.user.is_staff)
        )

class CompanyViewSet(viewsets.ViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Company.nodes.all()

    @swagger_auto_schema(
        operation_description="List all companies",
        responses={200: CompanySerializer(many=True)}
    )
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Retrieve a specific company by name",
        responses={200: CompanySerializer()}
    )
    def retrieve(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new company",
        query_serializer=CompanySerializer,
        responses={201: CompanySerializer()}
    )
    def create(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            company = Company(**serializer.validated_data).save()
            return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing company",
        query_serializer=CompanySerializer,
        responses={200: CompanySerializer()}
    )
    def update(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            updated_company = serializer.save()
            return Response(CompanySerializer(updated_company).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a company",
        responses={204: "No content"}
    )
    def destroy(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Get or add relationships for a company",
        methods=['get', 'post'],
        query_seralizer=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'related_company_name': openapi.Schema(type=openapi.TYPE_STRING),
                'relationship_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['SUPPLIES', 'PARTNERS_WITH', 'COMPETES_WITH']),
            },
            required=['related_company_name', 'relationship_type']
        ),
        responses={
            200: openapi.Response('Relationships retrieved successfully'),
            201: openapi.Response('Relationship added successfully'),
            400: 'Bad Request',
            404: 'Not Found'
        }
    )
    @action(detail=True, methods=['get', 'post'])
    def relationships(self, request, pk=None):
        try:
            company = Company.nodes.get(name=pk)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            relationships = {
                'suppliers': [{'name': c.name} for c in company.suppliers.all()],
                'customers': [{'name': c.name} for c in company.customers.all()],
                'partners': [{'name': c.name} for c in company.partners.all()],
                'competitors': [{'name': c.name} for c in company.competitors.all()],
            }
            return Response(relationships)

        elif request.method == 'POST':
            related_company_name = request.data.get('related_company_name')
            relationship_type = request.data.get('relationship_type')

            if not related_company_name or not relationship_type:
                return Response({'error': 'Missing related_company_name or relationship_type'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                related_company = Company.nodes.get(name=related_company_name)
            except Company.DoesNotExist:
                return Response({'error': 'Related company not found'}, status=status.HTTP_404_NOT_FOUND)

            if relationship_type == 'SUPPLIES':
                company.suppliers.connect(related_company)
            elif relationship_type == 'PARTNERS_WITH':
                company.partners.connect(related_company)
            elif relationship_type == 'COMPETES_WITH':
                company.competitors.connect(related_company)
            else:
                return Response({'error': 'Invalid relationship type'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': 'Relationship added'}, status=status.HTTP_201_CREATED)