# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals
from xyz_restful.mixins import UserApiMixin
from xyz_util.statutils import do_rest_stat_action, using_stats_db
from rest_framework.response import Response

__author__ = 'denishuang'
from . import models, serializers,stats, helper
from rest_framework import viewsets, decorators
from xyz_restful.decorators import register, register_raw


@register()
class DailyLogViewSet(UserApiMixin, viewsets.ModelViewSet):
    queryset = models.DailyLog.objects.all()
    serializer_class = serializers.DailyLogSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
    }

    @decorators.list_route(['POST'])
    def write(self, request):
        user = request.user
        for k, v in request.data.iteritems():
            log, created = models.DailyLog.objects.get_or_create(user=user, the_date=k)
            log.context.update(v)
            log.save()
        return Response({'detail': 'success'})


@register()
class StatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Stat.objects.all())
    serializer_class = serializers.StatSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull']
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_stat)

@register()
class RecordViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = using_stats_db(models.Record.objects.all())
    serializer_class = serializers.RecordSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'the_date': ['exact', 'gte', 'lte', 'range'],
        'metics': ['exact'],
        'owner_id': ['exact', 'isnull'],
        'owner_type': ['exact',],
        'user': ['exact',],
        'user_group': ['exact',],
        'owner_group': ['exact',]
    }

    @decorators.list_route(['get'])
    def stat(self, request):
        return do_rest_stat_action(self, stats.stats_record)

@register()
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = models.Performance.objects.all()
    serializer_class = serializers.PerformanceSerializer
    filter_fields = {
        'id': ['in', 'exact'],
        'update_time': ['exact', 'gte', 'lte', 'range'],
        'owner_id': ['exact', 'isnull', 'in'],
        'owner_type': ['exact',],
        'user': ['exact',],
        'user_group': ['exact',],
        'owner_group': ['exact',]
    }
    search_fields = ['owner_name', 'user_name', 'user_group', 'owner_group']

    @decorators.list_route(['GET'])
    def read(self, request):
        p = helper.get_performance(request.query_params, request.user)
        return Response(serializers.PerformanceSerializer(instance=p).data)

    @decorators.list_route(['POST'])
    def write(self, request):
        p = helper.save_performance(request.data, request.user)
        return Response(serializers.PerformanceSerializer(instance=p).data)

@register_raw(path='dailylog/object')
class ObjectViewSet(viewsets.ViewSet):

    @decorators.action(['get'], detail={}, permission_classes=[])
    def views(self, request):
        model = request.query_params.get('model')
        id = request.query_params.get('id')
        from .stores import ObjectLog
        ol = ObjectLog()
        ol.log(model, id)
        return Response({'detail': ol.query(model, id)})

