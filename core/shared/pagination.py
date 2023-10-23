from rest_framework.pagination import PageNumberPagination


def page_number_pagination_factory(
    page_size: int = None,
    max_page_size: int = None,
    page_size_query_param: str = "page_size"
) -> type[PageNumberPagination]:
    class PaginationClass(PageNumberPagination):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.page_size = page_size
            self.max_page_size = max_page_size
            self.page_size_query_param = page_size_query_param

    return PaginationClass
