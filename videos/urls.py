from django.urls import path
from .views import (
    VideoListView,
    VideoDetailView,
    VideoLikeView,
    VideoIdsView,
    VideoStatisticsSubqueryView,
    VideoStatisticsGroupByView,
)

urlpatterns = [
    path("v1/videos/", VideoListView.as_view(), name="video-list"),
    path("v1/videos/<int:pk>/", VideoDetailView.as_view(), name="video-detail"),
    path("v1/videos/<int:pk>/likes/", VideoLikeView.as_view(), name="video-likes"),
    path("v1/videos/ids/", VideoIdsView.as_view(), name="video-ids"),
    path("v1/videos/statistics-subquery/", VideoStatisticsSubqueryView.as_view(), name="video-stats-subquery"),
    path("v1/videos/statistics-group-by/", VideoStatisticsGroupByView.as_view(), name="video-stats-groupby"),
]