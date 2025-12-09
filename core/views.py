from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeviceDataSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserregistrationForm, DeviceForm
from .models import Device, DeviceData
from django.contrib import messages
from django.conf import settings
from dotenv import load_dotenv
from django.http import JsonResponse
import os
load_dotenv()



def home_view(request):
    return render(request, 'core/base.html')

def register_view(request):
    if request.method == 'POST':
         form = UserregistrationForm(request.POST)
         if form.is_valid():
              form.save()
              messages.success(request, "Registration successful. Please login.")
              return redirect('login')
         else: 
             messages.error(request, "Please correct the below error")
    else:
         form = UserregistrationForm()
    return render(request, 'core/register.html',{'form':form})


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.save()
            return redirect('dashboard')  # Refresh dashboard after adding device
    else:
        form = DeviceForm()

    devices = request.user.devices.all()
    return render(request, 'core/dashboard.html', {
        'devices': devices,
        'form': form
    })

@login_required
def device_data_json(request, device_id):
    device = get_object_or_404(Device, device_id=device_id, user=request.user)
    latest_data = DeviceData.objects.filter(device=device).order_by("-timestamp").first()

    if latest_data:
       return JsonResponse({
            "nitrogen": latest_data.nitrogen,
            "phosphorus": latest_data.phosphorus,
            "potassium": latest_data.potassium,
            "temperature": latest_data.temperature,
            "humidity": latest_data.humidity,
            "timestamp": latest_data.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        })
    else:
        return JsonResponse({"error": "No data found"}, status=404)

@login_required
def device_data_page(request, device_id):
    """Renders the HTML page with JS fetch"""
    return render(request, 'core/device_data.html', {"device_id": device_id})

@api_view(["POST"])
@permission_classes([])  # AllowAny for now; change to IsAuthenticated later
def push_single(request):
    serializer = DeviceDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([])  # allow any for now
def push_batch(request):
    """
    Expects JSON: {"readings": [ {device_id, nitrogen, phosphorus, ...}, {...} ]}
    """
    readings = request.data.get("readings")
    if not isinstance(readings, list):
        return Response({"error": "readings must be a list"}, status=status.HTTP_400_BAD_REQUEST)

    created = []
    errors = []
    for idx, item in enumerate(readings):
        serializer = DeviceDataSerializer(data=item)
        if serializer.is_valid():
            serializer.save()
            created.append(serializer.data)
        else:
            errors.append({"index": idx, "errors": serializer.errors})

    if errors:
        return Response({"created": created, "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
    return Response({"created": created}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([])
def get_device_data(request, device_id):

    device = get_object_or_404(Device, device_id = device_id)
    data = DeviceData.objects.filter(device=device).order_by("-timestamp")
    serializer = DeviceDataSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


#-------------------------------------------------------------New data vies-----------------------------------------------------------------------

@login_required
def device_latest_json(request, device_id):
    device = get_object_or_404(Device, device_id=device_id, user=request.user)
    latest = DeviceData.objects.filter(device=device).order_by("-timestamp").first()

    if not latest:
        return JsonResponse({"error": "No data found"}, status=404)

    return JsonResponse({
        "nitrogen": latest.nitrogen,
        "phosphorus": latest.phosphorus,
        "potassium": latest.potassium,
        "temperature": latest.temperature,
        "humidity": latest.humidity,
        "timestamp": latest.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    })

@login_required
def device_history_json(request, device_id):
    device = get_object_or_404(Device, device_id=device_id, user=request.user)
    data = (
        DeviceData.objects.filter(device=device)
        .order_by("-timestamp")[:10]
    )

    response = [
        {
            "nitrogen": d.nitrogen,
            "phosphorus": d.phosphorus,
            "potassium": d.potassium,
            "temperature": d.temperature,
            "humidity": d.humidity,
            "timestamp": d.timestamp.strftime("%H:%M:%S"),
        }
        for d in reversed(data) # show oldest → latest
    ]

    return JsonResponse({"history": response})
