import unittest

from werkzeug.exceptions import NotFound

from config import TestConfig
from adverts import create_app, db
from adverts.services import *
from adverts.models import *


class DatabaseTester(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()


class TestGetOne(DatabaseTester):
    def test_empty_db(self):
        for idx in range(10):
            self.assertRaises(NotFound, get_advertisement, idx)
        # DB should be still empty
        self.assertEqual(Advertisement.query.count(), 0)

    def test_filled_db(self):
        for i in range(0, 10, 2):
            advert = Advertisement(advert_id=i, title='t', description='', price=1)
            db.session.add(advert)
        else:
            db.session.commit()

        with self.subTest('Existent'):
            for i in range(0, 10, 2):
                advert = get_advertisement(i)
                self.assertIsNotNone(advert)
                self.assertEqual(advert.advert_id, i)

        with self.subTest('Nonexistent'):
            for i in range(1, 10, 2):
                self.assertRaises(NotFound, get_advertisement, i)


class TestCreation(DatabaseTester):
    def test_create_one(self):
        advert = create_advertisement('A title', 'A description', 495.0, ['link1', 'link2'])
        self.assertIsInstance(advert, Advertisement)
        self.assertEqual(advert.title, 'A title')
        self.assertEqual(advert.description, 'A description')
        self.assertEqual(advert.price, 495.0)

        self.assertEqual(len(advert.all_photos), 2)
        self.assertEqual(advert.all_photos[0].photo_link, 'link1')
        self.assertEqual(advert.all_photos[1].photo_link, 'link2')

    def test_multiple_creation(self):
        for i in range(10):
            create_advertisement('A title #{}'.format(i),
                                 'A description #{}'.format(i),
                                 10.0 * i,
                                 ['link{}'.format(i)] * i)
        self.assertEqual(Advertisement.query.count(), 10)
        self.assertEqual(Photo.query.count(), sum(range(10)))


class TestListings(DatabaseTester):
    def create_db(self):
        for i in range(15):
            create_advertisement(
                'A title #{}'.format(i),
                'A description #{}'.format(i),
                10.0 * (i % 7) + 50.0,
                ['link{}'.format(i)] * i
            )

    def test_get_all(self):
        self.create_db()
        expected = Advertisement.query.all()
        assert len(expected) == 15
        observed = get_advertisements_list(page=None)
        self.assertListEqual(observed, expected)

    def test_pagination(self):
        self.create_db()
        with self.subTest('Arbitrary page'):
            observed = get_advertisements_list(page=2, page_size=5)
            self.assertListEqual([a.advert_id for a in observed], [6, 7, 8, 9, 10])
        with self.subTest('Last page'):
            observed = get_advertisements_list(page=3, page_size=7)
            self.assertListEqual([a.advert_id for a in observed], [15])
        with self.subTest('Out of range page'):
            observed = get_advertisements_list(page=3, page_size=10)
            self.assertListEqual(observed, [])

    def test_orderings(self):
        self.create_db()
        with self.subTest('By creation', desc=False):
            observed = get_advertisements_list(page=1, page_size=3, order='date')
            self.assertListEqual([a.advert_id for a in observed], [1, 2, 3])
        with self.subTest('By creation', desc=True):
            observed = get_advertisements_list(page=1, page_size=3, order='date', desc=True)
            self.assertListEqual([a.advert_id for a in observed], [15, 14, 13])
        with self.subTest('By price', desc=False):
            observed = get_advertisements_list(page=1, page_size=4, order='price')
            self.assertListEqual([a.price for a in observed], [50., 50., 50., 60.])
        with self.subTest('By price', desc=True):
            observed = get_advertisements_list(page=1, page_size=3, order='price', desc=True)
            self.assertListEqual([a.price for a in observed], [110., 110., 100.])
