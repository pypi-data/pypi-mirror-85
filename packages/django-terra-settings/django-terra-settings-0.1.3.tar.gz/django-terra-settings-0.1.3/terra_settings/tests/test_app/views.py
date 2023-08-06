from rest_framework import generics

from terra_settings.filters import JSONFieldOrderingFilter
from terra_settings.tests.test_app.models import DummyModel
from terra_settings.tests.test_app.serializers import DummySerializer


class OrderingListView(generics.ListAPIView):
    permission_classes = ()
    queryset = DummyModel.objects.all().order_by('pk')
    serializer_class = DummySerializer
    filter_backends = (JSONFieldOrderingFilter,)
    ordering_fields = ['properties', ]
