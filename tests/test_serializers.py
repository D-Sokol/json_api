import unittest
from jsonschema import ValidationError

from adverts.serializers import *

class TestValidation(unittest.TestCase):
    def _assert_all_raises(self, examples, exc=ValidationError):
        for example in examples:
            self.assertRaises(ValidationError, validate_advert, example)

    def _assert_none_raises(self, examples):
        # Validation function either raises an exception or returns None object.
        # Therefore, conditions 'not raises' and 'returns None' are considered the same.
        # Do not use this function without this assumption.
        for example in examples:
            self.assertIsNone(validate_advert(example))

    def test_not_an_object(self):
        examples = [None, 495, 0.42, 'string', ['a', 'r', 'r', 'a', 'y']]
        self._assert_all_raises(examples)

    def test_not_enough_fields(self):
        bad = [
            {},
            # No price
            {'title': 'Snake', 'description': 'Sell a snake', 'photo_links': ['http://example.com/images/1.png']},
            # No description
            {'title': 'Snake', 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']},
            # No title
            {'price': 1000.0, 'description': 'Sell a snake', 'photo_links': ['http://example.com/images/1.png']},
        ]
        good = [
            # No photos is allowed.
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 1000.0},
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 1000.0, 'photo_links': []},
        ]
        self._assert_all_raises(bad)
        self._assert_none_raises(good)

    def test_extra_fields(self):
        base = {'title': 'Snake', 'description': 'Sell a snake', 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']}
        self._assert_none_raises((base,))
        additional_fields = [None, 495, 0.42, 'string', ['a', 'r', 'r', 'a', 'y']]
        for additional in additional_fields:
            base['info'] = additional
            self.assertRaises(ValidationError, validate_advert, base)

    def test_strings_too_long(self):
        bad = [
            {'title': 'S'*201, 'description': 'Sell a snake', 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']},
            {'title': 'Snake', 'description': 'S'*1001, 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']},
        ]
        good = [
            {'title': 'S'*200, 'description': 'S'*1000, 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']},
        ]
        self._assert_all_raises(bad)
        self._assert_none_raises(good)

    def test_price_is_not_positive(self):
        bad = [
            {'title': 'Snake', 'description': 'Sell a snake', 'price': -50.0, 'photo_links': ['http://example.com/images/1.png']},
            {'title': 'Snake', 'description': 'Sell a snake', 'price': None, 'photo_links': ['http://example.com/images/1.png']},
        ]
        good = [
            {'title': 'S'*200, 'description': 'S'*1000, 'price': 0, 'photo_links': ['http://example.com/images/1.png']},
            {'title': 'S'*200, 'description': 'S'*1000, 'price': 0., 'photo_links': ['http://example.com/images/1.png']},
            {'title': 'S'*200, 'description': 'S'*1000, 'price': 1000.0, 'photo_links': ['http://example.com/images/1.png']},
            {'title': 'S'*200, 'description': 'S'*1000, 'price': 1000, 'photo_links': ['http://example.com/images/1.png']},
        ]
        self._assert_all_raises(bad)
        self._assert_none_raises(good)

    def test_too_many_photos(self):
        bad = [
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 42, 'photo_links':
                ['http://example.com/images/{}.png'.format(i) for i in range(1, 10)]},
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 42, 'photo_links':
                ['http://example.com/images/{}.png'.format(i) for i in (1, 2, 3, 4)]},
        ]
        good = [
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 42, 'photo_links':
                ['http://example.com/images/1.png']},
            {'title': 'Snake', 'description': 'Sell a snake', 'price': 42, 'photo_links':
                ['http://example.com/images/{}.png'.format(i) for i in (1, 2, 3)]},
        ]
        self._assert_all_raises(bad)
        self._assert_none_raises(good)
