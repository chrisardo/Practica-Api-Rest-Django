'''
from django.core.paginator import EmptyPage


def paginator(dara, page, per_page):
    paginator = Paginator(dara, per_page)
    try:
        data = paginator.page(page)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    return data
    '''
