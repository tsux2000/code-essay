from re import search


DEFAULT_ORDER = '-create_date'


class OrderAndPageConverter:

    """
    パラメータからorder（並び順）とpage（ページ）を取得するためのコンバータ.
    """

    regex = '((order/[a-z0-9_\-]+/)|(page/[0-9]+/)){0,2}'

    def to_python(self, value):
        order = search(r'order/([a-z0-9_\-]+)/', value)
        self.order = str(order[1]) if order else DEFAULT_ORDER
        page = search(r'page/([0-9]+)/', value)
        self.page = str(page[1]) if page else '1'
        self.page = self.page if int(self.page) else '1'
        return self.order, self.page

    def to_url(self, value):
        return str(value)
