from rest_framework.permissions import BasePermission


class IsStaffOrOwnerOrPublished(BasePermission):
    """Permission used for list/retrieve: allow access if:
    - request.user.is_staff -> allowed
    - request.user is owner of the video -> allowed
    - video.is_published -> allowed
    Note: this permission expects view.get_object() or queryset filtering for list.
    """


    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if obj.is_published:
            return True
        return obj.owner == request.user