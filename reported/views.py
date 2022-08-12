from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from login_signup.class_and_functions import *
from .models import *
# Create your views here.


@api_view(['POST', ])
def report_video_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            video_id= request.data['video_id']
            report_type = int(request.data['report_type'])
            video_obj = MediaTable.objects.get(pk=video_id)
            possible_reportobj = ReportTypes.objects.filter(for_what='P')
            possible_report=[]
            for i in possible_reportobj:
                possible_report.append(i.id)
            if report_type in possible_report:
                pass
            else:
                data["code"] = 0
                data["error"] = True
                data["message"] = "Please provide a valid report type"
                return Response(data=data)
            report_type = ReportTypes.objects.get(id=report_type)
            user_obj=User.objects.get(id=user_id)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please provide a valid data"
            return Response(data=data)
        try:
            obj = PostReportHistory(post=video_obj,reported_by=user_obj,report_type=report_type)
            obj.save()
            data["code"] = 0
            data["error"] = False
            data["message"] = "Video reported successfully"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Something went wrong"
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)



@api_view(['POST', ])
def report_user_view(request):
    data = {}
    if authentication_check(request) is True:
        user_id = get_id_from_auth(request)
        try:
            user= int(request.data['user_id'])
            user_obj1 = User.objects.get(id=user)
            report_type = ReportTypes.objects.get(id=5)
            user_obj=User.objects.get(id=user_id)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Please provide a valid data"
            return Response(data=data)
        if user_obj1.is_active is False:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry user dosen't exist or removed"
            return Response(data=data)
        if user_obj1 == user_obj:
            data['code'] = 0
            data['error'] = True
            data['message'] = "Sorry you can't report yourself"
            return Response(data=data)
        try:
            obj = UserReportHistory(reported_user=user_obj1,reported_by=user_obj,report_type=report_type)
            obj.save()
            data["code"] = 0
            data["error"] = False
            data["message"] = "User reported successfully"
            return Response(data=data)
        except:
            data["code"] = 0
            data["error"] = True
            data["message"] = "Something went wrong"
            return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)


@api_view(['POST', ])
def video_report_type_view(request):
    data = {}
    if authentication_check(request) is True:
        possible_report_obj = ReportTypes.objects.filter(for_what='P')
        report_list = []
        for report_obj in possible_report_obj:
            temp_dict = {}
            temp_dict['id'] = report_obj.id
            temp_dict['name'] = report_obj.name
            report_list.append(temp_dict)
        data["code"] = 0
        data["error"] = False
        data["message"] = ""
        data["data"] = report_list
        return Response(data=data)
    else:
        data['code'] = 0
        data['message'] = "Authorization error"
        data['error'] = True
        return Response(status=status.HTTP_401_UNAUTHORIZED,data=data)
