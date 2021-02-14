from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from requests import Response
from rest_framework import viewsets, generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Company, CompanyBank, Medicine, MedicalDetail
from .serializers import CompanySerializer, CompanyBankSerializer, MedicineSerializer, MedicalDetailSerializer, \
    MedicalDetailSerializerSimple


class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def list(self, request):
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True, context={"request": request})
        response_dic = {"error": False, "message": "All Company List Data", "data": serializer.data}
        return Response(response_dic)

    @staticmethod
    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            dic_response = {"error": False, "message": "Company Data Save Successful"}
        except:
            dic_response = {"error": False, "message": "Error During Saving Company Data"}
        return Response(dic_response)

    @staticmethod
    def update(self, request, pk=None):
        try:
            queryset = Company.objects.all()
            company = get_object_or_404(queryset, pk=pk)
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid()
            serializer.save()
            dic_response = {"error": False, "message": "Company Data Update Successful"}
        except:
            dic_response = {"error": True, "message": "Error During Updating  Company Data"}
        return Response(dic_response)


class CompanyBankViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def create(self, request):
        try:
            serializer = CompanySerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            dict_response = {"error": False, "massage": "Company Bank Data Save Successfully"}

        except:
            dict_response = {"error": True, "message": "Error During Saving Company Bank Data "}
        return Response(dict_response)

    @staticmethod
    def list(self, request):
        company_bank = CompanyBank.objects.all()
        serializer = CompanyBankSerializer(company_bank, many=True, context={"request": request})
        response_dic = {"error": False, "message": "All Company Bank List Data", "data": serializer.data}
        return Response(response_dic)

    @staticmethod
    def retrieve(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        company_bank = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company_bank, context={"request": request})
        return Response({"error": False, "message": "Single Data Patch", "data": serializer.data})

    @staticmethod
    def update(self, request, pk=None):
        queryset = CompanyBank.objects.all()
        company_bank = get_object_or_404(queryset, pk=pk)
        serializer = CompanyBankSerializer(CompanyBank, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data has been Updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerializer

    def get_queryset(self):
        name = self.kwargs["name"]
        return Company.objects.filter(name=name)


class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def create(self, request):
        try:
            serializer = MedicineSerializer(data=request.data, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            medicine_id = serializer.data['id']
            medicine_details_list = []
            for medicine_detail in request.data["medicine_details"]:
                medicine_detail["medicine_id"] = medicine_id
                medicine_details_list.append(medicine_detail)
            serializer2 = MedicalDetailSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()
            dict_response = {"error": False, "massage": "Medicine Data Save Successfully"}

        except:
            dict_response = {"error": True, "message": "Error During Saving Medicine Data "}
        return Response(dict_response)

    @staticmethod
    def list(self, request):
        medicine = Medicine.objects.all()
        serializer = MedicineSerializer(medicine, many=True, context={"request": request})
        medicine_data = serializer.data
        new_medicine_list = []
        for medicine in medicine_data:
            medicine_details = MedicalDetail.objects.filter(medicine_id = medicine["id"])
            medicine_details_serializer = MedicalDetailSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"] = medicine_details_serializer.data
            new_medicine_list.append(medicine)
        response_dic = {"error": False, "message": "All Medicine List Data", "data": serializer.data}
        return Response(response_dic)

    @staticmethod
    def retrieve(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, context={"request": request})
        serializer_data = serializer.data
        medicine_details = MedicalDetail.objects.filter(medicine_id = serializer_data["id"])
        medicine_details_serializers = MedicalDetailSerializerSimple(medicine_details,many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data
        return Response({"error": False, "message": "Single Data Patch", "data": serializer_data})

    @staticmethod
    def update(self, request, pk=None):
        queryset = Medicine.objects.all()
        medicine = get_object_or_404(queryset, pk=pk)
        serializer = MedicineSerializer(medicine, data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()
        return Response({"error": False, "message": "Data has been Updated"})


company_list = CompanyViewSet.as_view({"get": "list"})

company_create = CompanyViewSet.as_view({"post": "create"})

company_update = CompanyViewSet.as_view({"put": "update"})
