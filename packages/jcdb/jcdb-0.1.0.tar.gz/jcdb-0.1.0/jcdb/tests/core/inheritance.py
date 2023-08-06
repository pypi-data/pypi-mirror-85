from unittest import TestCase

from jcdb import Object


class Inheritant(Object):

    """
    An inheriting dummy class.
    """


Object.register(Inheritant)


class TestInheritance(TestCase):

    """
    Test object properties on inheritance.
    """

    ## --- init --- ##

    def test_init(self):

        i = Inheritant()

    ## --- encoding --- ##

    def test_encode_basic(self):

        i = Inheritant()
        self.assertEquals(i.encode(), '{"_type": "Inheritant"}')

    ## --- decoding --- ##

    def test_decode_basic(self):

        i = Inheritant()
        self.assertEquals(i, Inheritant.decode(i.encode()))
