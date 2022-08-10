from rest_framework import mixins, viewsets


class ListCreateDestroyViewset(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
