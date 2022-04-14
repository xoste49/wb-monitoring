import datetime

from rest_framework import filters

from .models import Articles
from .validators import checking_required_validator, interval_validator


class ProductHistoryFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        article = request.query_params.get('article')
        checking_required_validator(article, 'article')
        from_date = request.query_params.get('from_date')
        checking_required_validator(from_date, 'from_date')
        to_date = request.query_params.get('to_date')
        checking_required_validator(to_date, 'to_date')
        interval = request.query_params.get('interval')
        checking_required_validator(interval, 'interval')
        from_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        from_date = datetime.datetime.combine(from_date, datetime.time.min)
        to_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        to_date = datetime.datetime.combine(to_date, datetime.time.max)
        interval = int(interval)
        interval_validator(interval)
        queryset = Articles.objects.get(article=article)
        queryset = queryset.history.filter(
            add_date__range=(from_date, to_date))
        if interval == 1:
            hours = [x for x in range(0, 24)]
            return queryset.filter(add_date__hour__in=hours)
        elif interval == 12:
            return queryset.filter(add_date__hour__in=(0, 30))
        elif interval == 24:
            return queryset.filter(add_date__hour=0)
        return queryset
