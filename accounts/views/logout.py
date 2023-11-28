from dj_rest_auth.views import LogoutView


class LogoutAPIView(LogoutView):
    http_method_names = ('post',)
    serializer_class = None
