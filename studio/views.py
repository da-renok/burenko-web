from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ConflictError
from .models import Design, Master
from .serializers import DesignSerializer, MasterSerializer


class DesignListView(APIView):
    def get(self, request):
        designs = Design.objects.all()
        style = request.query_params.get("style")
        if style:
            designs = designs.filter(style__iexact=style)
        serializer = DesignSerializer(designs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DesignDetailView(APIView):
    def get_object(self, pk):
        try:
            return Design.objects.get(pk=pk)
        except Design.DoesNotExist:
            raise NotFound(f"Ескіз з id={pk} не знайдено.")

    def get(self, request, pk):
        serializer = DesignSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = DesignSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        design = self.get_object(pk)
        data = DesignSerializer(design).data
        design.delete()
        return Response(data)


class MasterListView(APIView):
    def get(self, request):
        serializer = MasterSerializer(Master.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MasterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MasterDetailView(APIView):
    def get_object(self, pk):
        try:
            return Master.objects.get(pk=pk)
        except Master.DoesNotExist:
            raise NotFound(f"Майстра з id={pk} не знайдено.")

    def get(self, request, pk):
        serializer = MasterSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = MasterSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        master = self.get_object(pk)
        designs_count = master.designs.count()
        if designs_count:
            raise ConflictError(
                f"Неможливо видалити майстра «{master.name}», оскільки "
                f"за ним закріплено ескізів: {designs_count}. "
                "Спершу видаліть ці ескізи або змініть їхнього майстра."
            )
        data = MasterSerializer(master).data
        master.delete()
        return Response(data)
