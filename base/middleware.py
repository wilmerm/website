
from base.models import VisitCounter


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        self.set_visit(request)
        request.visit_class = VisitCounter
        request.visits_on_current_path = VisitCounter.objects.filter(urlpath=request.path)
        return None
    
    def process_template_response(self, request, response):
        return response

    def set_visit(self, request):
        if (request.user.is_superuser) or (request.user.is_staff):
            return

        try:
            visit_counter = VisitCounter.on_today(urlpath=request.path)
        except (VisitCounter.DoesNotExist):
            visit_counter = VisitCounter(urlpath=request.path)
            try:
                visit_counter.clean()
            except (BaseException) as e:
                print(e)
                return

            visit_counter.count += 1
            try:
                visit_counter.save()
            except (BaseException) as e:
                print(e)
                return