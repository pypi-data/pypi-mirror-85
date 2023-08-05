from datetime import datetime
from rest_framework.decorators import (action)
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .func import get_tree
from .jwt_token import jwt_get_userid_handler, jwt_get_openid_handler, jwt_get_unionid_handler


class CustomModelViewSet(ModelViewSet):
    model_class = None

    # filterset_fields = {
    #     '_type': {
    #         'type': 'int',
    #         'filter': ''
    #     },
    #     'title': {
    #         'type': 'string',
    #         'filter': '__contains'
    #     },
    #     'extend__is_banner': {
    #         'type': 'boolean',
    #         'filter': ''
    #     },
    # }
    filterset_fields = {}

    def get_queryset(self):
        queryset = self.model_class.objects.all()

        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        if self.filterset_fields:
            for key in self.filterset_fields:
                field_value = self.request.query_params.get(key, None)
                if field_value:
                    # 字段存在查询
                    if key == '_exists':
                        field_value = field_value.split(',')
                        for i in field_value:
                            lookup_type = i + '__exists'
                            queryset = queryset.filter(
                                **{lookup_type: True})

                    else:
                        _filter = self.filterset_fields[key]
                        if _filter['filter'] == '__in':
                            field_value = field_value.split(',')
                            if _filter['type'] == 'int':
                                field_value = [int(i) for i in field_value]

                        if _filter['type'] == 'boolean':
                            if field_value == 'true':
                                field_value = True
                            elif field_value == 'false':
                                field_value = False

                        lookup_type = key + _filter['filter']
                        queryset = queryset.filter(
                            **{lookup_type: field_value})
        return queryset

    def perform_update(self, serializer):
        serializer.save(updated=datetime.now())


def user_perform_create(token, serializer):
    user_id = jwt_get_userid_handler(token)
    openid = jwt_get_openid_handler(token)
    unionid = jwt_get_unionid_handler(token)
    serializer.save(user_id=user_id, openid=openid, unionid=unionid)


class TreeAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        parent = request.query_params.get('parent', None)
        data = get_tree(serializer.data, parent)
        return Response(data)


class AllView:

    @action(detail=False, methods=['get'], url_path='all', url_name='all')
    def all(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
