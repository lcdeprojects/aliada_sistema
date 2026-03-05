from django.shortcuts import render

def group_required(*group_names):
    """
    Decorator for views that checks whether a user has a group membership,
    rendering an access denied page if not allowed.
    Usage: @group_required('group1', 'group2')
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                if user.groups.filter(name__in=group_names).exists() or user.is_superuser:
                    return view_func(request, *args, **kwargs)
            return render(request, 'core/access_denied.html', status=403)
        return _wrapped_view
    return decorator
