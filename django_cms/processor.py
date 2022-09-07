from django.conf import settings


# global variable that can be accesed in template

def setting(request):
    return {
            "host": f" {request.scheme}://{request.get_host()}",
            "cannonical_url": request.build_absolute_uri(request.path),
        }
