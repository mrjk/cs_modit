from flask import Flask, current_app, request, url_for
from flask_paginate import Pagination, get_page_args, get_parameter


#
# ==============================================================


#
# ==============================================================


#
# ==============================================================


# Misc: Pagination
# ==============================================================

class Paginate(Pagination):

    def __init__(self, model, page=None, per_page=None, **kwargs ):

        if per_page < 1:
            per_page=None

        paginated = model.paginate(page=page, per_page=per_page)

        self.paginated=paginated
        self.items=paginated.items

        print (paginated.page, paginated.per_page, paginated.total)

        super().__init__(
            p=paginated.page,
            pp=paginated.per_page,
            page_parameter="p",
            per_page_parameter="pp",
            total=paginated.total,
            css_framework="bootstrap4",
            link_size="sm",
            alignment="center",
            show_single_page=True,
            **kwargs
        )


    def generate_pp(self, sizes=(25,50,100,-1), show_all=True):

        html = '<ul class="pagination pagination-sm">'
        for i in sizes:
            active='active' if i == self.per_page  else ''
            html += '<li class="page-item {}"><a class="page-link" href="{}?'.format(active, url_for('workshop.mod_list'))

            params=dict(request.args)
            params[self.per_page_parameter]=i
            if i < 0:
                params[self.page_parameter]=1
            html += '&'.join(['{}={}'.format(k,v) for k,v in params.items()])
            html += '" >%s</a></li>' % (i if i > 0 else 'All')

        html += "</ul>"
        return html




#
# ==============================================================



#
# ==============================================================



#
# ==============================================================


#
# ==============================================================