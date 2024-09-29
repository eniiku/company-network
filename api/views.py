from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company
from .serializers import CompanySerializer

class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in ['GET', 'HEAD', 'OPTIONS'] or is_admin

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.nodes.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'industry', 'founded_year']
    ordering_fields = ['name', 'founded_year']
    
    def get_object(self):
        try:
            return Company.nodes.get(name=self.kwargs['pk'])
        except Company.DoesNotExist:
            return None
        
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data) 

    def retrieve(self, request, pk=None):
        try:
            company = self.get_object()
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
            company = self.get_object()
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            company = serializer.save()
            return Response(CompanySerializer(company).data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            company = self.get_object()
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)
        company.delete()
        return Response(status=204)
        
    @action(detail=True, methods=['get', 'post'])
    def relationships(self, request, pk=None):
        company = self.get_object()
        if request.method == 'GET':
            relationships = {
                'suppliers': [{'name': c.name} for c in company.suppliers.all()],
                'customers': [{'name': c.name} for c in company.customers.all()],
                'partners': [{'name': c.name} for c in company.partners.all()],
                'competitors': [{'name': c.name} for c in company.competitors.all()],
            }
            return Response(relationships)
        elif request.method == 'POST':
            if not company:
                return Response({'error': 'Company not found'}, status=404) 