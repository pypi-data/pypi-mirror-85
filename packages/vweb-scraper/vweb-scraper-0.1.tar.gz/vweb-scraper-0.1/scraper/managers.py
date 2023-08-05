import typing

import settings


class ScraperManager:
    PRODUCT_URL_MIDDLEWARE = settings.MIDDLEWARES["PRODUCT_URL_MIDDLEWARE"]
    MESSENGER_FUNCTION = None
    REQUEST_MANAGER = None
    LOGGER = None
    PRODUCT_LIST_PAGE_URLS = []
    REQUIRED_KEYWORDS = []
    product_list_page_count = 0

    PRODUCT_DETAIL_PAGE_TEMPLATE = {
        "restock": "",
        "product_image": "",
        "product_price": "",
        "product_url": "",
        "product_brand": "",
        "product_name": "",
        "product_sizes": "",
        "product_colors": ""
    }

    def __init__(
            self, request_manger=None, logger=None,
            check_restock=False
    ):
        self.request_manager = request_manger or self.REQUEST_MANAGER
        self.logger = logger or self.LOGGER

        self.addons = []

        self.check_restock = check_restock
        self.product_data = {} if check_restock else set()
        self.current_product = None

    def get_product_urls(self) -> typing.Generator:
        """This must yield product urls scraped from the product list page."""
        raise ValueError("Override ``get_product_urls`` method to yield product detail page urls.")

    def get_product_detail(self, product_url: str) -> dict:
        """This must yield product detail data scraped from the product detail page.

        Must return dict with following keys
          * restock: bool = False,
          * product_image: (list, str) = None,
          * product_price: str = None,
          * product_url: str = None,
          * product_brand: str = None,
          * product_name: str = None,
          * product_sizes: (list, str) = None,
          * product_colors: (list, str) = None
        """
        raise ValueError("Override ``get_product_detail`` to return product details as mentioned above.")

    def get_product_detail_template(self, **kwargs):
        return {**self.PRODUCT_DETAIL_PAGE_TEMPLATE, **kwargs}

    def handler(self, func, default="", *args):
        try:
            return func()
        except (ValueError, KeyError, AttributeError, IndexError, *args) as e:
            self.logger(e)
            return default

    def get_product_list_page_urls(self):
        return self.PRODUCT_LIST_PAGE_URLS

    def get_messenger_function(self):
        messenger = getattr(self, self.MESSENGER_FUNCTION, None)
        assert messenger is not None, (
            "either provide messenger function name in ``MESSENGER_FUNCTION`` or override ``get_messenger_function``"
            "and return function object which contains required parameters for sending message."
        )
        return messenger

    def default_diff_checker(self):
        messenger = self.get_messenger_function()

        if self.check_restock:
            product_url = self.current_product.get("product_url")

            if product_url in self.product_data:
                if self.product_data[product_url] != self.current_product:
                    messenger(restock=True, **self.current_product)
                    return
            else:
                messenger(restock=False, **self.current_product)
                return
        else:
            if self.current_product not in self.product_data:
                messenger(restock=False, **self.get_product_detail(self.current_product))
                return

    def check_diff(self, checker="default"):
        diff_checker = getattr(self, f"{checker}_diff_checker")
        assert diff_checker is not None, f"``{checker}_diff_checker`` Function not found."
        diff_checker()

    def validate(self, data):
        for keyword in self.REQUIRED_KEYWORDS:
            if keyword in data:
                return True
        return False

    def __run(self, first):
        self.product_list_page_count = 0

        for url in self.get_product_urls():
            if self.check_restock:
                product_detail = self.get_product_detail(product_url=url)

                # For validating keywords !!
                if not self.validate(product_detail.get("product_name")):
                    continue

                self.current_product = product_detail
                if not first:
                    self.check_diff()
                self.product_data[url] = product_detail
            else:
                self.current_product = url
                if not first:
                    self.check_diff()
                self.product_data.add(url)

    def run(self, infinite=True, iterations=99):
        first = True

        if infinite:
            while True:
                self.__run(first)
                first = False
        else:
            for i in range(iterations):
                self.__run(first)
                first = False

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)
