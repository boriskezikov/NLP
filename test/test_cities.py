import unittest

from Lab2.constants import ADDRESS
from Lab2.extractor import extract


class TestCity(unittest.TestCase):

    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('липецк', 'город'))

    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('сургут', None))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('липецк', 'город'))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_6(self):
        testing_address = 'сургут югорская 30/2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('сургут', None))

    def test_7(self):
        testing_address = 'индекс 12 мне вот этого не надо'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_8(self):
        testing_address = 'ты сургут улица 30 лет победы'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('сургут', None))

    def test_9(self):
        testing_address = 'надо 50% город нальчик горького 1257'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('нальчик', 'город'))

    def test_10(self):
        testing_address = 'null'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_11(self):
        testing_address = '60 мегабит я'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_12(self):
        testing_address = 'сургут крылова 53/4'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('сургут', None))

    def test_13(self):
        testing_address = 'так москва хамовнический вал но я думаю что я еще обсужу со своими домашними ' \
                          'то есть вот у нас цифровое телевидение есть но акадо вот вы не спешите я тогда ' \
                          'вам наберу но либо в приложения'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), ('москва', None))

    def test_14(self):
        testing_address = 'мое 3 парковая'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_15(self):
        testing_address = 'Пришвина 17'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))

    def test_16(self):
        testing_address = 'Старый Гай 1 корпус 2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((res['city'], res['city_type']), (None, None))


if __name__ == '__main__':
    unittest.main()
