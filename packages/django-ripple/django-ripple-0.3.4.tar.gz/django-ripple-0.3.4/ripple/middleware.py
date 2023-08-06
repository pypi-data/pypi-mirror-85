from datetime import timedelta
import re
from django.conf import settings

from django.core import signing
from django.core.signing import TimestampSigner
from django.http import HttpResponse, HttpResponseNotFound

from .models import FeatureOption
from django.core.cache import cache

url_re = re.compile(settings.PRIVATE_URL_RE)
exceptions_re = settings.PRIVATE_URL_EXCEPTION_RE and re.compile(settings.PRIVATE_URL_EXCEPTION_RE)


class TesterMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

        # One-time configuration and initialization.
        # raise MiddlewareNotUsed

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        passkey = request.GET.get('pass', None )
        signer = TimestampSigner()
        request.session['features'] = []
        if not (request.path.startswith('/admin/')
                or request.path in ['/healthcheck', '/robots.txt', '/troubleshoot', '/account/verify']
                or (exceptions_re and exceptions_re.match(request.path))
                or passkey in settings.PRIVATE_URL_ACCESS_KEYS
                ):

            fo = cache.get('featureoptions')

            if fo is None:
                fo = [{'name': f.name, 'urls_re': [re.compile(u.regex) for u in f.urls.all()]}
                      for f in FeatureOption.objects.filter(active=True).all()]
                cache.set('featureoptions', fo, 3600)

            if settings.PRIVATE_URL_RE:
                fo.append({'name': 'site-settings', 'urls_re': [url_re]})

            for f in fo:
                block = True
                if f['name'] in request.COOKIES:
                    value = request.COOKIES[f['name']]
                    try:
                        value = signer.unsign(value, max_age=timedelta(days=2))
                        block = False
                        request.session['features'].append(f['name'])
                    except signing.BadSignature:
                        pass

                if 'staff' in request.COOKIES:
                    try:
                        signer.unsign(
                            request.COOKIES['staff'], max_age=timedelta(days=7))
                        block = False
                    except signing.BadSignature:
                        pass

                for key in settings.PRIVATE_URL_ACCESS_KEYS:
                    if key in request.COOKIES:
                        try:
                            signer.unsign(
                                request.COOKIES[key], max_age=timedelta(hours=settings.PRIVATE_URL_ACCESS_TIME))
                            block = False
                        except signing.BadSignature:
                            pass

                if block and not request.user.is_staff:
                    for u in f['urls_re']:
                        if u.match(request.path):
                            return HttpResponse(f'<h1>Not Found {request.path}</h1>')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        if hasattr(request, 'user') and request.user.is_staff:
            response.set_cookie('staff', signer.sign('staff'), max_age=86400*7)
        if passkey in settings.PRIVATE_URL_ACCESS_KEYS:
            response.set_cookie(passkey, signer.sign(passkey), max_age=settings.PRIVATE_URL_ACCESS_TIME*3600)

        return response
