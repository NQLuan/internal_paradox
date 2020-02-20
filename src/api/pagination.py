#!/usr/bin/env python

# author Huy 
# date 8/26/2019
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'previous': self.get_previous_link(),
                'next': self.get_next_link(),
            },
            'current': self.page.number,
            'page_size': self.page_size,
            'page_number': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'results': data
        })
