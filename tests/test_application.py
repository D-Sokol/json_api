import unittest

from config import TestConfig
from adverts import create_app, app, db
# Create_advertisement considered as already tested, so it is used here to create content in db.
from adverts.services import create_advertisement


class HTTPTester(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # All API functions registered in the original adverts.app object, not in new self.app.
        # These lines is a hack to copy endpoints.
        self.app.url_map = app.url_map
        self.app.view_functions = app.view_functions

        self.client = self.app.test_client
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    @staticmethod
    def _link(index=1):
        return 'http://example.com/images/{}.png'.format(index)

    def fill_database(self):
        create_advertisement('Snake', 'Sell a snake', 495.0, [self._link(11), self._link(12)])
        create_advertisement('Invisible Pink Unicorn', 'Sell an unicorn. Sorry, no photo -- it is invisible!', 20.0, [])
        create_advertisement('A cat', 'Give a cat in a good hands', 0.0, [self._link(31)])

    def post(self, path, *args, **kw):
        return self.client().post(path, *args, **kw)

    def get(self, path, *args, **kw):
        return self.client().get(path, *args, **kw)


class TestGetItem(HTTPTester):
    def test_exists_or_not(self):
        self.fill_database()
        for index in range(6):
            exists = (index in (1, 2, 3))
            resp = self.get('/advertisement/{}'.format(index))
            self.assertEqual(resp.status_code, 200 if exists else 404)

    def test_item_found_correct(self):
        pass

    def test_additional_fields(self):
        pass


class TestItemList(HTTPTester):
    def test_pages(self):
        pass

    def test_order(self):
        pass


class TestCreateItem(HTTPTester):
    def test_bad_examples(self):
        pass

    def test_good_examples(self):
        pass
