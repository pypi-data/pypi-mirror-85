from djangoldp.views import LDPViewSet
from djangoldp.pagination import LDPPagination


class LDPNotificationsPagination(LDPPagination):
    default_limit = 100


class LDPNotificationsViewSet(LDPViewSet):
    '''overridden LDPViewSet to force pagination'''
    pagination_class = LDPNotificationsPagination
