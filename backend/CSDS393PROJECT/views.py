from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import ProfileSerializer, EventSerializer, AttendanceSerializer
from .models import UserProfile, Event, Attendance
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse
# Create your views here.

#class ProfileView(viewsets.ModelViewSet):
 #   serializer_class = ProfileSerializer
  #  queryset = UserProfile.objects.all()

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
@api_view(['GET','POST'])
def ProfileView(request):

    if request.method == 'GET':
        data = UserProfile.objects.all()
        serializer = ProfileSerializer (data, context = {'request':request}, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
@ensure_csrf_cookie
@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
def ProfileUpdate(request, pk):
    try:
        profile = UserProfile.objects.get(pk=pk)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        profile.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

            
    
@ensure_csrf_cookie
@api_view(['GET','POST', 'PUT'])
def EventView(request):
    if request.method == 'GET':
        data = Event.objects.all()
        serializer = EventSerializer (data, context = {'request':request}, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        serializer = EventSerializer(date = request.data)


@ensure_csrf_cookie
@api_view (['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def EventUpdate(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PATCH':
        serializer = ProfileSerializer(event, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = EventSerializer(event, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        event.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


    #if(text_method == 'GET')
    #input 
    #data = UserProfile.objects.get(username== input)
    #serializer = ~~~
    #return Response (serializer.data)

@api_view(['GET', 'POST'])
def AttendanceView(request):
    if request.method == 'GET':
        data = Attendance.objects.all()
        serializer = AttendanceSerializer (data, context = {'request':request}, many = True)
        events = Event.objects.filter(pk = 1)
        print('hello')
        #print(events)
        #print(Attendance.getAttendees(events))
        #print(Attendance.objects.filter(is_attending = True))
        #print(Attendance.objects.filter(attendee = 1))
        #join call matching username and created_by
        # to do this probably need to make creator a foreign key reference to UserProfile
        return Response(serializer.data)
      
    elif request.method == 'POST':
        #keys for dictionary should be event, attendee, is_attending
        #manually load in and serialize the data to then put into model and save record of Attendance to db
        attendance_dict = json.loads(request.data)
        if('event' in attendance_dict):
            eventName = attendance_dict['event']
        else:return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if('attendee' in attendance_dict):
            attendeeName = attendance_dict['attendee']
        else:return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if('is_attending' in attendance_dict):
            is_attending = attendance_dict['is_attending']
        else:return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.get(name = eventName)
        profile = UserProfile.objects.get(username = attendeeName)
        a = Attendance(profile, event, is_attending)
        a.save()
        return Response(serializer.errors, status=status.HTTP_201_CREATED)

#view that shows all attendees of an event
@api_view(['GET'])
def AttendingEvent(request, event_name):
        queryset = Attendance.getAttending(event_name)
        list1 = list(queryset)
        serialized_q = json.dumps(list1, cls = DjangoJSONEncoder)
        return Response(serialized_q)

@api_view(['GET'])
def EventsAttending(request, profile_name):
    queryset = Attendance.getEvents(profile_name)
    serialized_q = json.dumps(list(queryset), cls = DjangoJSONEncoder)
    return Response(serialized_q)

@api_view(['DELETE', 'GET', 'POST', 'PATCH'])
def changeAttending(request, event_name, profile_name):
    try:
        attendance = Attendance.objects.get(event__name = event_name, attendee__profileName = profile_name)
    except Attendance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        attendance.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
    

    
    elif request.method == 'PATCH':
        serializer = AttendanceSerializer(attendance, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_202_ACCEPTED)
        
    return Response(status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def CreatedEvents(request, user_name):
    events = Event.createdEvents(user_name)
    #serializer = EventSerializer(events)
    list1 = list(events)
    serialized_events = json.dumps(list1, cls = DjangoJSONEncoder)
    return Response (serialized_events)