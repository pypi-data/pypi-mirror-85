from unittest import TestCase

from jcdb import *


class TestObject(TestCase):

    """
    Test basic object en / decoding.
    """

    ## --- Initialisation --- ##

    def test_init(self):

        o = Object()

    def test_setters(self):

        o = Object()
        o.attr_1 = 1
        o.attr_2 = Object()

    ## --- Encoding --- ##

    def test_encode_basic(self):

        o = Object()
        self.assertEquals(o.encode(), '{"_type": "Object"}')

    def test_encode_attr(self):

        o = Object()
        o.attr_1 = 1
        o.attr_2 = "hi"
        self.assertEquals(
            o.encode(), '{"_type": "Object", "attr_1": 1, "attr_2": "hi"}'
        )

    def test_encode_attr_obj(self):

        o = Object()
        o.attr_1 = 1
        o.attr_2 = Object()
        self.assertEquals(
            o.encode(),
            '{"_type": "Object", "attr_1": 1, "attr_2": {"_type": "Object"}}',
        )

    ## --- Decoding --- ##

    def test_decode_basic(self):

        o = Object()
        self.assertEquals(o, Object.decode(o.encode()))

    def test_decode_attr(self):

        o = Object()
        o.a = "a"
        o.num = 45959
        o.x = {"lll": "3", "ll": 2, "l": 1}
        self.assertEquals(o, Object.decode(o.encode()))

    def test_decode_attr_obj(self):

        o = Object()
        o.a = "a"
        o.num = 45959
        o.obj = Object()
        o.obj.a = "a"
        o.obj.obj = Object()
        self.assertEquals(o, Object.decode(o.encode()))
