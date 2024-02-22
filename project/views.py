from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Company, Employee, Question, Result, KnowledgeArea
from .serializers import (
    CompanySerializer,
    EmployeeSerializer,
    QuestionSerializer,
    ResultSerializer,
    CompanyCreateSerializer,
    KnowladgeSerializer, QuestionGetSerializer, CompanyNameSerializer, ResultGet, EmployeeGetSerializer
)
from core.models import User
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import status

from django.db.models import Sum

@api_view(['GET'])
def calculate_all_domain_averages_percent(request):
    company_id = request.GET.get('company_id')
    employee_id = request.GET.get('employee_id')

    if company_id and employee_id:
        results = (
            Result.objects
            .filter(company_id=company_id, employee_id=employee_id)
            .aggregate(total_number=Sum('total_number'), result=Sum('result'))
        )

        total_number = results.get('total_number', 0)
        result = results.get('result', 0)

        if total_number != 0:
            average = result / total_number
            average_percent = (result / total_number) * 100
        else:
            average = 0
            average_percent = 0

        data = {
            'average': average,
            'percent': average_percent/4
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Please provide company_id and employee_id parameters'})

@api_view(['GET'])
def calculate_all_domain_averages(request):
    company_id = request.GET.get('company_id')
    employee_id = request.GET.get('employee_id')

    if company_id and employee_id:
        results = (
            Result.objects
            .filter(company_id=company_id, employee_id=employee_id)
            .values('domain')
            .annotate(total_number=Sum('total_number'), result=Sum('result'))
        )

        domain_averages = {}
        for domain_data in results:
            domain = domain_data['domain']
            total_number = domain_data.get('total_number', 0)
            result = domain_data.get('result', 0)
            if total_number != 0:
                average = result / total_number
            else:
                average = 0
            domain_averages[domain] = {'total_number': total_number, 'result': result, 'average': average}

        return JsonResponse(domain_averages)
    else:
        return JsonResponse({'error': 'Please provide company_id and employee_id parameters'})

@api_view(['POST'])
def user_detail(request):
    if request.method == 'POST':
        data = request.data
        user_id = data.get("id")
        try:
            user = User.objects.get(id=user_id)
            if user.user_type == 'employee':
                try:
                    employee = Employee.objects.get(user=user)
                    company = employee.company
                    company_serializer = CompanyNameSerializer(company)
                    return Response({'company': company_serializer.data, "employee": employee.id, "survey": user.survey}, status=status.HTTP_200_OK)
                except Employee.DoesNotExist:
                    # Return a 404 response if employee record not found
                    return Response({'error': 'Employee record not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                try:
                    company = Company.objects.get(user=user)
                    company_serializer = CompanySerializer(company)  # Serialize the Company object
                    return Response({'company': company_serializer.data}, status=status.HTTP_200_OK)
                except Company.DoesNotExist:
                    return Response({'error': 'Company record not found'}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def survey_status(request):
    if request.method == 'POST':
        data = request.data
        id = data.get('id')
        survey = data.get('survey')

        user = User.objects.get(id=id)
        user.survey = survey
        user.save()
        return Response({"message": "Submitted successfully!"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def calculate_domain_averages(request):
    company_id = request.GET.get('company_id')
    employee_id = request.GET.get('employee_id')

    if company_id and employee_id:
        # Define process groups excluding "oe"
        process_groups = ['initiating', 'planning', 'executing', 'm&c', 'closing']

        results = (
            Result.objects
            .filter(company_id=company_id, employee_id=employee_id)
            .exclude(domain='oe')  # Exclude "oe" domain
            .exclude(process_group__isnull=True)  # Exclude null process groups
            .values('process_group')
            .annotate(total_number=Count('id'), result=Count('result'))
            .order_by('process_group')
        )

        domain_averages = {}
        for process_group_data in results:
            total_number = process_group_data.get('total_number', 0)
            if total_number != 0:
                average = process_group_data['result'] / total_number
                domain_averages[process_group_data['process_group']] = {
                    'process_group': process_group_data['process_group'],
                    'average': average
                }

        # Fill in missing process groups with zero averages
        for process_group in process_groups:
            if process_group not in domain_averages:
                domain_averages[process_group] = {'process_group': process_group, 'average': 0}

        return JsonResponse(domain_averages)
    else:
        return JsonResponse({'error': 'Please provide company_id and employee_id parameters'})

    
@api_view(['GET'])
def calculate_oe_domain_averages(request):
    company_id = request.GET.get('company_id')
    employee_id = request.GET.get('employee_id')

    if company_id and employee_id:
        # Define stages excluding "oe"
        stages = ["human-resources", "cultural", "technological", "structural"]

        results = (
            Result.objects
            .filter(company_id=company_id, employee_id=employee_id, domain='oe')
            .values('stage')
            .annotate(total_number=Count('id'), result=Count('result'))
            .order_by('stage')
        )

        domain_averages = {}
        for stage_data in results:
            total_number = stage_data.get('total_number', 0)
            if total_number != 0:
                average = stage_data['result'] / total_number
                domain_averages[stage_data['stage']] = {
                    'stage': stage_data['stage'],
                    'average': average
                }

        # Fill in missing stages with zero averages
        for stage in stages:
            if stage not in domain_averages:
                domain_averages[stage] = {'stage': stage, 'average': 0}

        return JsonResponse(domain_averages)
    else:
        return JsonResponse({'error': 'Please provide company_id and employee_id parameters'})
    
    
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyCreateSerializer
        return CompanySerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

class EmployeeViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Employee.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id, user__survey="taken")
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeSerializer
        return EmployeeGetSerializer

class KnowledgeAreaViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeArea.objects.all()
    serializer_class = KnowladgeSerializer
    
class QuestionViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionSerializer
        return QuestionGetSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        knowledge_area_name = self.request.query_params.get('knowledge_area_name')
        stage = self.request.query_params.get('stage')
        domain = self.request.query_params.get('domain')

        if knowledge_area_name and stage and domain:
            # Assuming knowledge_area_name is unique
            knowledge_area = KnowledgeArea.objects.filter(name=knowledge_area_name).first()
            if knowledge_area:
                queryset = queryset.filter(knowledge_area=knowledge_area,stage=stage, domain=domain)

        elif stage:
            queryset = queryset.filter(stage=stage)
            
        elif domain:
            queryset = queryset.filter(domain=domain)

        return queryset

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    def get_serializer_class(self):
        if self.action == 'create':
            return ResultSerializer
        return ResultGet

    def get_queryset(self):
        company_id = self.request.query_params.get('company_id')
        employee_id = self.request.query_params.get('employee_id')
        stage = self.request.query_params.get('stage')
        domain = self.request.query_params.get('domain')
        knowledge_area = self.request.query_params.get('knowledge_area')
        
        if company_id and employee_id and domain and knowledge_area:
            return Result.objects.filter(company_id=company_id, employee_id=employee_id, domain=domain, knowledge_area__isnull=False)
        if company_id and employee_id and domain:
            return Result.objects.filter(company_id=company_id, employee_id=employee_id, domain=domain)
        elif company_id and employee_id and stage:
            return Result.objects.filter(company_id=company_id, employee_id=employee_id, stage=stage)
        elif company_id:
            return Result.objects.filter(company_id=company_id)
        elif employee_id:
            return Result.objects.filter(employee_id=employee_id)
        else:
            return Result.objects.all()
