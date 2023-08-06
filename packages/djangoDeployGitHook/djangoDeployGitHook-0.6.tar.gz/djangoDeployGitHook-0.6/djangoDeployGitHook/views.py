import logging
import os
from ipaddress import ip_address, ip_network
from pathlib import Path

from django.conf import settings
from django.contrib.sites import requests
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger('django')


# Create your views here.
@require_POST
@csrf_exempt
def githookA2HostingCloneUpdate(request):
    # Verify if request came from GitHub
    # forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    # logger.debug("HTTP_X_FORWARDED_FOR: "+forwarded_for)
    # if forwarded_for is None:
    #    forwarded_for = u'{}'.format(request.META.get('REMOTE_ADDR'))
    # logger.debug("REMOTE_ADDR: "+forwarded_for)

    # for k_meta, v_meta in request.META.items():
    #     logger.debug("k_meta: " + k_meta)
    #     logger.debug("v_meta: " + v_meta)

    # client_ip_address = ip_address(forwarded_for)
    # whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    # for valid_ip in whitelist:
    #    if client_ip_address in ip_network(valid_ip):
    #   break
    # else:
    #    return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # Deploy some code for example
        import subprocess
        process = subprocess.Popen(['git', 'pull'])
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        from django.core.management import call_command
        call_command('migrate')
        call_command('collectstatic', interactive=False)

        logger.debug(settings.BASE_DIR)
        full_path_touch = os.path.join(settings.BASE_DIR, "tmp/restart.txt")
        logger.debug(full_path_touch)
        Path(full_path_touch).touch()

        return HttpResponse('success')
    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)

@require_POST
@csrf_exempt
def githookA2HostingRemoteUpdate(request):
    # Verify if request came from GitHub
    # forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))
    # logger.debug("HTTP_X_FORWARDED_FOR: "+forwarded_for)
    # if forwarded_for is None:
    #    forwarded_for = u'{}'.format(request.META.get('REMOTE_ADDR'))
    # logger.debug("REMOTE_ADDR: "+forwarded_for)

    # for k_meta, v_meta in request.META.items():
    #     logger.debug("k_meta: " + k_meta)
    #     logger.debug("v_meta: " + v_meta)

    # client_ip_address = ip_address(forwarded_for)
    # whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    # for valid_ip in whitelist:
    #    if client_ip_address in ip_network(valid_ip):
    #   break
    # else:
    #    return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # Deploy some code for example
        import subprocess
        process = subprocess.Popen(['git', 'pull','origin','master'])
        #git submodule update --recursive --remote -f
        process = subprocess.Popen(['git', 'submodule','update','-recursive','--remote','-f'])
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        from django.core.management import call_command
        call_command('migrate')
        call_command('collectstatic', interactive=False)

        logger.debug(settings.BASE_DIR)
        full_path_touch = os.path.join(settings.BASE_DIR, "tmp/restart.txt")
        logger.debug(full_path_touch)
        Path(full_path_touch).touch()

        return HttpResponse('success')
    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)


@require_POST
@csrf_exempt
def test_githook(request):
    # Verify if request came from GitHub

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')

    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)


@require_POST
@csrf_exempt
def githookRaspberry(request):
    # Verify if request came from GitHub
    forwarded_for = u'{}'.format(request.META.get('HTTP_X_FORWARDED_FOR'))

    client_ip_address = ip_address(forwarded_for)

    whitelist = requests.get('https://api.github.com/meta').json()['hooks']

    for valid_ip in whitelist:
        if client_ip_address in ip_network(valid_ip):
            break
    else:
        return HttpResponseForbidden('Permission denied.')

    # If request reached this point we are in a good shape
    # Process the GitHub events
    event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

    if event == 'ping':
        return HttpResponse('pong')
    elif event == 'push':
        # Deploy some code for example
        import subprocess
        process = subprocess.Popen(['git', 'pull'])
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

        from django.core.management import call_command
        call_command('migrate')
        call_command('collectstatic', interactive=False)

        subprocess.call(["sudo", "systemctl", "reload", "gunicorn"])
        subprocess.call(["sudo", "systemctl", "reload", "nginx"])

        return HttpResponse('success')
    # In case we receive an event that's not ping or push
    return HttpResponse(status=204)


def test_update(request):
    return HttpResponse('Hello, From DjangoDeployGitHook!')


