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
        self.fill_database()
        with self.subTest('1'):
            resp = self.get('/advertisement/1')
            data = resp.get_json()
            expected = {'title': 'Snake', 'price': 495.0, 'main_photo': self._link(11)}
            self.assertDictEqual(data, expected)
        with self.subTest('2'):
            resp = self.get('/advertisement/2')
            data = resp.get_json()
            expected = {'title': 'Invisible Pink Unicorn', 'price': 20.0, 'main_photo': None}
            self.assertDictEqual(data, expected)
        with self.subTest('3'):
            resp = self.get('/advertisement/3')
            data = resp.get_json()
            expected = {'title': 'A cat', 'price': 0.0, 'main_photo': self._link(31)}
            self.assertDictEqual(data, expected)

    def test_additional_fields(self):
        self.fill_database()
        with self.subTest('All fields'):
            resp = self.get('/advertisement/1', query_string={'fields': 'all_photos,description'})
            data = resp.get_json()
            self.assertIsInstance(data, dict)
            self.assertEqual(data.get('description'), 'Sell a snake')
            self.assertListEqual(data.get('all_photos'), [self._link(11), self._link(12)])
        with self.subTest('Only description'):
            resp = self.get('/advertisement/1', query_string={'fields': 'description'})
            data = resp.get_json()
            self.assertIsInstance(data, dict)
            self.assertIn('description', data)
            self.assertNotIn('all_photos', data)
        with self.subTest('Only photos'):
            resp = self.get('/advertisement/1', query_string={'fields': 'all_photos'})
            data = resp.get_json()
            self.assertIsInstance(data, dict)
            self.assertNotIn('description', data)
            self.assertIn('all_photos', data)
        with self.subTest('No additional fields'):
            resp = self.get('/advertisement/1', query_string={'fields': ''})
            data = resp.get_json()
            self.assertIsInstance(data, dict)
            self.assertNotIn('description', data)
            self.assertNotIn('all_photos', data)


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
