import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import ConflictError
from .models import Design, Master
from .serializers import DesignSerializer, MasterSerializer

logger = logging.getLogger(__name__)


class DesignListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("style", OpenApiTypes.STR, OpenApiParameter.QUERY)
        ],
        responses={200: DesignSerializer(many=True)},
    )
    def get(self, request):
        designs = Design.objects.all()
        style = request.query_params.get("style")
        if style:
            designs = designs.filter(style__iexact=style)
        serializer = DesignSerializer(designs, many=True)
        logger.info("Отримано список ескізів (%d)", len(serializer.data))
        return Response(serializer.data)

    @extend_schema(
        request=DesignSerializer,
        responses={
            201: DesignSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        serializer = DesignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        design = serializer.save()
        logger.info("Створено ескіз id=%d", design.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DesignDetailView(APIView):
    def get_object(self, pk):
        try:
            return Design.objects.get(pk=pk)
        except Design.DoesNotExist:
            raise NotFound(f"Ескіз з id={pk} не знайдено.")

    @extend_schema(responses={200: DesignSerializer, 404: OpenApiTypes.OBJECT})
    def get(self, request, pk):
        serializer = DesignSerializer(self.get_object(pk))
        return Response(serializer.data)

    @extend_schema(
        request=DesignSerializer,
        responses={
            200: DesignSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    )
    def put(self, request, pk):
        serializer = DesignSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        design = serializer.save()
        logger.info("Оновлено ескіз id=%d", design.id)
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: DesignSerializer,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        }
    )
    def delete(self, request, pk):
        design = self.get_object(pk)
        data = DesignSerializer(design).data
        design.delete()
        logger.info("Видалено ескіз id=%d", pk)
        return Response(data)


class MasterListView(APIView):
    @extend_schema(responses={200: MasterSerializer(many=True)})
    def get(self, request):
        serializer = MasterSerializer(Master.objects.all(), many=True)
        logger.info("Отримано список майстрів (%d)", len(serializer.data))
        return Response(serializer.data)

    @extend_schema(
        request=MasterSerializer,
        responses={
            201: MasterSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
        },
    )
    def post(self, request):
        serializer = MasterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        master = serializer.save()
        logger.info("Створено майстра id=%d", master.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MasterDetailView(APIView):
    def get_object(self, pk):
        try:
            return Master.objects.get(pk=pk)
        except Master.DoesNotExist:
            raise NotFound(f"Майстра з id={pk} не знайдено.")

    @extend_schema(responses={200: MasterSerializer, 404: OpenApiTypes.OBJECT})
    def get(self, request, pk):
        serializer = MasterSerializer(self.get_object(pk))
        return Response(serializer.data)

    @extend_schema(
        request=MasterSerializer,
        responses={
            200: MasterSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
        },
    )
    def put(self, request, pk):
        serializer = MasterSerializer(self.get_object(pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        master = serializer.save()
        logger.info("Оновлено майстра id=%d", master.id)
        return Response(serializer.data)

    @extend_schema(
        responses={
            200: MasterSerializer,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT,
            409: OpenApiTypes.OBJECT,
        }
    )
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
        logger.info("Видалено майстра id=%d", pk)
        return Response(data)
