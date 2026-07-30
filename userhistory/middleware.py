from django.utils import timezone

from .models import UserActivity


class UserHistoryMiddleware:
    IGNORED_PREFIXES = ('/static/', '/media/', '/admin/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        previous_visit = request.COOKIES.get('last_visit')
        request.session['previous_visit'] = previous_visit
        request.session['visit_count'] = request.session.get('visit_count', 0) + 1

        response = self.get_response(request)

        if self._should_track(request, response):
            UserActivity.objects.create(
                user=request.user,
                path=request.path,
                page_name=self._page_name(request.path),
                method=request.method,
            )

        response.set_cookie(
            'last_visit',
            timezone.localtime().strftime('%B %d, %Y, %I:%M %p').replace(' 0', ' '),
            max_age=60 * 60 * 24 * 30,
            samesite='Lax',
        )
        return response

    def _should_track(self, request, response):
        if response.status_code >= 400:
            return False
        if request.path.startswith(self.IGNORED_PREFIXES):
            return False
        return request.user.is_authenticated

    def _page_name(self, path):
        if path == '/':
            return 'Home'
        parts = [part for part in path.strip('/').split('/') if part]
        if not parts:
            return 'Home'
        return ' '.join(part.replace('-', ' ').title() for part in parts[:2])
