from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Server
from celery.result import AsyncResult
import simplejson


def dashboard(request):
    return HttpResponse('dashboard')


def send_command(request):
    if request.method == 'POST':
        if 'data' not in request.POST:
            return HttpResponse(status=400)
        else:
            data = simplejson.JSONDecoder().decode(request.POST['data'])
            server = Server.objects.get(uuid=data['uuid'])
            proc_id = server.execute_or_none(request.user, data['command'])
            if server.execute_or_none(request.user, data['command']): # execute_or_none returns a celery task id if
                return JsonResponse({'proc_id': proc_id})
            else:
                return HttpResponse(status=403)

    return HttpResponse(status=405)

def check_proc(request):
    if request.method == 'POST':
        if 'proc_id' in request.POST:
            async_result = AsyncResult(request.POST['proc_id'])
            try:
                result = async_result.get(timeout=5, propagate=False)
            except TimeoutError:
                result = None
            status = async_result.status
            if isinstance(result, Exception):
                return JsonResponse({
                    'status': status,
                    'error': str(result)
                })
            else:
                return JsonResponse({
                    'status': status,
                    'result': result
                })
        else:
            return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)
