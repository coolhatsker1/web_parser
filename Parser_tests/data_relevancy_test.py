import unittest
# from main import get_page_data
import validators

CATEGORY_URL = "https://www.gorgany.com/odiah/shtany"
class test_parser(unittest.TestCase):
    def test_url(self) -> None:
        assert validators.url(CATEGORY_URL)

    # def test_page_respone(self) -> None:
    #     assert get_page_data(CATEGORY_URL)