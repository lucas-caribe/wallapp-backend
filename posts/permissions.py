from rest_framework import permissions

class PostPermissions(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.user.is_superuser:
      return True

    if view.action == 'list' or view.action == 'retrieve':
      return True
    elif view.action == 'create':
      return request.user.is_authenticated
    else:
      return False

  def has_object_permission(self, request, view, obj):
    if not request.user.is_authenticated:
      return False

    if view.action == 'retrieve':
      return True
    elif view.action in ['update', 'partial_update', 'destroy']:
      return obj.owner == request.user or request.user.is_superuser
    else:
      return False
