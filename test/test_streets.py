import unittest

from Lab2.extractor import *


class TestStreet(unittest.TestCase):

    def test_1(self):
        testing_address = 'проспект комсомольский 50'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('комсомольский', 'проспект'), (res['street'], res['street_type']))

    def test_2(self):
        testing_address = 'город липецк улица катукова 36 a'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('катукова', 'улица'), (res['street'], res['street_type']))

    def test_3(self):
        testing_address = 'сургут улица рабочая дом 31а'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('рабочая', 'улица'), (res['street'], res['street_type']))

    def test_4(self):
        testing_address = 'город липецк доватора 18'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('доватора', None), (res['street'], res['street_type']))

    def test_5(self):
        testing_address = 'ну бехтеева 9 квартира 310'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('бехтеева', None), (res['street'], res['street_type']))

    def test_6(self):
        testing_address = 'улица меркулова дом 24'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('меркулова', 'улица'), (res['street'], res['street_type']))

    def test_7(self):
        testing_address = 'октябрьская 48 частный дом город сургут'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('октябрьская', None), (res['street'], res['street_type']))

    def test_8(self):
        testing_address = 'сколько улица 30 лет победы 50 46'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('30 лет победы', 'улица'), (res['street'], res['street_type']))

    def test_9(self):
        testing_address = 'тюменский тракт 10'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('тюменский', 'тракт'), (res['street'], res['street_type']))

    def test_10(self):
        testing_address = 'сургут югорская 30/2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('югорская', None), (res['street'], res['street_type']))

    def test_11(self):
        testing_address = 'индекс 12 мне вот этого не надо'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((None, None), (res['street'], res['street_type']))

    def test_12(self):
        testing_address = 'старый оскол микрорайон олимпийский дом 23 квартира 105'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('олимпийский', 'микрорайон'), (res['street'], res['street_type']))

    def test_13(self):
        testing_address = 'город сургут улица фармана салманова 4'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('фармана салманова', 'улица'), (res['street'], res['street_type']))

    def test_14(self):
        testing_address = 'ты сургут улица 30 лет победы'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('30 лет победы', 'улица'), (res['street'], res['street_type']))

    def test_15(self):
        testing_address = 'проезд мунарева 2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('мунарева', 'проезд'), (res['street'], res['street_type']))

    def test_16(self):
        testing_address = 'домашний адрес где я живу'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((None, None), (res['street'], res['street_type']))

    def test_17(self):
        testing_address = 'артема 32 квартира 8'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('артема', None), (res['street'], res['street_type']))

    def test_18(self):
        testing_address = 'знаете знаете у меня дорогая девочка у меня уже все есть и менять из из одного ' \
                          'переходить на другой я не хочу поэтому какой город квартира какой ничего я вам ' \
                          'сообщать не хочу поэтому до свидания я ничего не'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((None, None), (res['street'], res['street_type']))

    def test_19(self):
        testing_address = 'новогиреевская 34'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('новогиреевская', None), (res['street'], res['street_type']))

    def test_20(self):
        testing_address = 'мое 3 парковая'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('парковая', None), (res['street'], res['street_type']))

    def test_21(self):
        testing_address = 'москва мусы джалиля 38 корпус 2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('мусы джалиля', None), (res['street'], res['street_type']))

    def test_22(self):
        testing_address = 'надо 50% город нальчик горького 1257'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('горького', None), (res['street'], res['street_type']))

    def test_23(self):
        testing_address = 'сколько стоит нет arkadata у нас есть москва каширское шоссе 55 корпус 1'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('каширское', 'шоссе'), (res['street'], res['street_type']))

    def test_24(self):
        testing_address = 'зеленые аллеи город видное дом 8'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('зеленые', 'аллеи'), (res['street'], res['street_type']))

    def test_25(self):
        testing_address = 'дмитрия ульянова 17 корпус 1 москва'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('дмитрия ульянова', None), (res['street'], res['street_type']))

    def test_26(self):
        testing_address = 'null'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((None, None), (res['street'], res['street_type']))

    def test_27(self):
        testing_address = 'стол вы знаете москва алтуфьевское 78'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('алтуфьевское', None), (res['street'], res['street_type']))

    def test_28(self):
        testing_address = 'марша захарова 12 маршала захарова дом 12'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('маршала захарова', None), (res['street'], res['street_type']))

    def test_29(self):
        testing_address = 'а зачем'
        res = extract(testing_address, ADDRESS)
        self.assertEqual((None, None), (res['street'], res['street_type']))

    def test_30(self):
        testing_address = 'Кавказский 16'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('Кавказский', None), (res['street'], res['street_type']))

    def test_31(self):
        testing_address = 'Старый Гай 1 корпус 2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('Старый Гай'.lower(), None), ((res['street'], res['street_type'])[0].lower(), None))

    def test_32(self):
        testing_address = 'зелинского улица зелинского дом 2'
        res = extract(testing_address, ADDRESS)
        self.assertEqual(('зелинского', 'улица'), (res['street'], res['street_type']))


if __name__ == '__main__':
    unittest.main()
