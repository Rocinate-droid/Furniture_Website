import uuid

class AnonymousCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.session.get('user_id'):
                request.session['user_id'] = str(uuid.uuid4())
        return self.get_response(request)