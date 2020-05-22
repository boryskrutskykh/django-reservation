from django.urls import path
from .views import HallList, HallDetail, reserve_table, check_free_table

urlpatterns = [
    path('', HallList.as_view(), name='hall_list'),
    path('hall/<slug:hall_slug>/', HallDetail.as_view(), name='hall_detail'),
    path('ajax/check_free_tables/', reserve_table, name='reserve_table'),
    path('ajax/free_tables/', check_free_table, name='check_free_table'),
]
