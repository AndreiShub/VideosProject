from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q, F, Count, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError


from .models import Video, Like
from .serializers import VideoSerializer
from .pagination import VideoPagination
from .permissions import IsStaffOrOwnerOrPublished
from django.contrib.auth import get_user_model


User = get_user_model()

class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer
    pagination_class = VideoPagination


    def get_queryset(self):
        user = self.request.user
        qs = Video.objects.all().prefetch_related("files").select_related("owner")
        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_published=True) | Q(owner=user))
        return qs.filter(is_published=True)

class VideoDetailView(generics.RetrieveAPIView):
    serializer_class = VideoSerializer


    def get_queryset(self):
        user = self.request.user
        qs = Video.objects.all().prefetch_related("files").select_related("owner")
        if user.is_staff:
            return qs
        if user.is_authenticated:
            return qs.filter(Q(is_published=True) | Q(owner=user))
        return qs.filter(is_published=True)

class VideoLikeView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, pk):
    # Add like - only for published videos (unless owner/staff?) requirement: for published videos
        video = get_object_or_404(Video, pk=pk)
        if not video.is_published and not (request.user.is_staff or video.owner == request.user):
            return Response({"detail": "Video is not available for liking."}, status=404)


        try:
            with transaction.atomic():
                like, created = Like.objects.get_or_create(video=video, user=request.user)
            if not created:
            # Already liked
                return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)
            # atomic increment to avoid race
            Video.objects.filter(pk=video.pk).update(total_likes=F("total_likes") + 1)
        except IntegrityError:
            return Response({"detail": "Conflict or duplicate"}, status=status.HTTP_409_CONFLICT)


        return Response({"detail": "Like added"}, status=status.HTTP_201_CREATED)


    def delete(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        if not video.is_published and not (request.user.is_staff or video.owner == request.user):
            return Response({"detail": "Video is not available."}, status=404)


        deleted, _ = Like.objects.filter(video=video, user=request.user).delete()
        if deleted:
        # decrement safely (avoid negative)
            Video.objects.filter(pk=video.pk, total_likes__gt=0).update(total_likes=F("total_likes") - 1)
            return Response({"detail": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"detail": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

class VideoIdsView(APIView):
    permission_classes = [IsAdminUser]


    def get(self, request):
        ids = list(Video.objects.filter(is_published=True).values_list("id", flat=True))
        return Response(ids)

class VideoStatisticsSubqueryView(APIView):
    permission_classes = [IsAdminUser]


    def get(self, request):
        # get per-user like counts using subquery
        like_count = (
        Like.objects.filter(user=OuterRef("pk"))
        .order_by()
        .values("user")
        .annotate(cnt=Count("id"))
        .values("cnt")
        )
        qs = User.objects.annotate(likes_count=Subquery(like_count[:1])).values("username", "likes_count")
        return Response(list(qs))

class VideoStatisticsGroupByView(APIView):
    permission_classes = [IsAdminUser]


    def get(self, request):
        qs = (
        User.objects.filter(likes__isnull=False)
        .annotate(likes_count=Count("likes"))
        .values("username", "likes_count")
        .order_by("-likes_count")
        )
        return Response(list(qs))