from django.db.models import Q
from djangoldp.filters import LDPPermissionsFilterBackend
from djangoldp_circle.xmpp import get_client_ip, XMPP_SERVERS
from rest_framework_guardian.filters import ObjectPermissionsFilter


class CircleFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous:
            return queryset.filter(status='Public')
        else:
            objects = super().filter_queryset(request, queryset, view).values_list('pk')
            return queryset.filter(
                Q(members__user=request.user) |
                Q(status='Public') |
                Q(pk__in=objects)
            ).distinct()


class CircleMemberFilterBackend(ObjectPermissionsFilter):
    def filter_queryset(self, request, queryset, view):
        if get_client_ip(request) in XMPP_SERVERS:
            return queryset
        elif request.user.is_anonymous:
            return super().filter_queryset(request, queryset, view)
        else:
            objects = super().filter_queryset(request, queryset, view).values_list('pk')
            return queryset.filter(
                Q(user=request.user) |
                Q(circle__status='Public') |
                Q(circle__members__user=request.user) |
                Q(pk__in=objects)
            ).distinct()
