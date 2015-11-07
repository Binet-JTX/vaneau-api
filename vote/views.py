import time, json, hashlib
from urllib import parse

from rest_framework import viewsets, decorators
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny

from vote.models import *

FKZ_KEY = b"ksj87sh0hsb14xn98"

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @decorators.list_route(methods=['post'])
    @decorators.permission_classes((AllowAny, ))
    def frankiz_auth_check(self, request):
        import logging
        logger = logging.getLogger(__name__)

        student = None
        response_data = {'valid': True, 'student': student}
        RETURN_PAGE = request.data.get('page', 'http://jtx/vaneau/').encode()
        logger.error(RETURN_PAGE)

        if not "timestamp" in request.query_params.keys() or not "response" in request.query_params.keys() or not "hash" in request.query_params.keys():
            logger.error('KEYS')
            response_data["valid"] = False

        response = parse.unquote_to_bytes(request.query_params.get("response"))
        ts = parse.unquote_to_bytes(request.query_params.get("timestamp"))
        h = parse.unquote_to_bytes(request.query_params.get("hash"))

        if abs(int(time.time()) - int(ts)) > 3600*3 or abs(int(ts) + 3*3600 - int(time.time())) < 30*60:
            logger.error('TS')
            response_data["valid"] = False

        if hashlib.md5(ts + FKZ_KEY + response).hexdigest() != h.decode():
            logger.error('HASH')
            response_data["valid"] = False

        if response_data["valid"]:
            data = json.loads(response.decode())
            try:
                student = Student.objects.get(hruid=data["hruid"])
            except Student.DoesNotExist:
                student = Student.objects.create(hruid=data["hruid"], lastname=data["lastname"], firstname=data["firstname"], promo=data["promo"])
            finally:
                response_data["student"] = StudentSerializer(student).data

        return Response(response_data, 200)

    @decorators.list_route(methods=['post'])
    @decorators.permission_classes((AllowAny, ))
    def frankiz_url(self, request):
        ts = str(int(time.time())).encode()
        page = request.data.get('page', 'http://jtx/vaneau/').encode()
        r = json.dumps(["names","promo"]).encode()
        h = hashlib.md5(ts + page + FKZ_KEY + r).hexdigest()
        return Response("http://www.frankiz.net/remote?" + parse.unquote(parse.urlencode([('timestamp',ts),('site',page),('hash',h),('request',r)])), 200)

# Function to verifiy if the requester has been authenticated by Frankiz
def frankiz_check(request):
    import logging
    logger = logging.getLogger(__name__)

    if not "timestamp" in request.query_params.keys() or not "response" in request.query_params.keys() or not "hash" in request.query_params.keys():
        logger.error('KEYS')
        raise NotAuthenticated()

    response = parse.unquote_to_bytes(request.query_params.get("response"))
    ts = parse.unquote_to_bytes(request.query_params.get("timestamp"))
    h = parse.unquote_to_bytes(request.query_params.get("hash"))

    if abs(int(time.time()) - int(ts)) > 3600*3:
        logger.error('TS')
        raise NotAuthenticated()

    if hashlib.md5(ts + FKZ_KEY + response).hexdigest() != h.decode():
        logger.error('HASH')
        raise NotAuthenticated()

    data = json.loads(response.decode())

    return request

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = (AllowAny, )
    filter_fields = ('category', 'student',)

    def retrieve(self, request, pk=None):
        try:
            request = frankiz_check(request)
        except NotAuthenticated:
            return Response("Not authenticated", 401)

        return super(VoteViewSet, self).retrieve(request, pk)

    def create(self, request):
        try:
            request = frankiz_check(request)
        except NotAuthenticated:
            return Response("Not authenticated", 401)

        return super(VoteViewSet, self).create(request)

    def update(self, request, pk=None):
        try:
            request = frankiz_check(request)
        except NotAuthenticated:
            return Response("Not authenticated", 401)

        return super(VoteViewSet, self).update(request, pk)

    def destroy(self, request, pk=None):
        try:
            request = frankiz_check(request)
        except NotAuthenticated:
            return Response("Not authenticated", 401)

        return super(VoteViewSet, self).destroy(request, pk)
