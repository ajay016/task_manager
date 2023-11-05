import django_filters
from .models import *

class TaskFilter(django_filters.FilterSet):
    # title__icontains = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')
    creation_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    due_date = django_filters.DateFilter(field_name='due_date', lookup_expr='exact')
    priority = django_filters.ChoiceFilter(
        field_name='priority',
        choices=Task.PRIORITY_CHOICES,
        # empty_label='Select Priority',
        # label='Priority'
    )
    # is_complete = django_filters.BooleanFilter()
    is_complete = django_filters.ChoiceFilter(
        field_name='is_complete',
        choices=[
            (True, 'Completed'),
            (False, 'Not Completed'),
        ],
    )

    class Meta:
        model = Task
        # fields = ['title__icontains', 'creation_date', 'due_date', 'priority', 'is_complete']
        # fields = '__all__'
        fields = ['created_at', 'due_date', 'priority', 'is_complete']