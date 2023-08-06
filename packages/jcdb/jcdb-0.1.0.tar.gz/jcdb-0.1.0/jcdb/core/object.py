import json


class Object:

    """
    JCDB Objects can be stored, serialized and manipulated in many ways.
    """

    ## --- De / Encoder Classes --- ##

    class Encoder(json.JSONEncoder):

        """
        JCDB Object Encoder / Serializer.
        """

        def default(self, obj):

            """
            Makes objects serializable and stores their types.
            """

            return {"_type": type(obj).__name__, **obj.__dict__}

    class Decoder(json.JSONDecoder):

        """
        JCDB Object Decoder / Deserializer.
        """

        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(
                self, object_hook=self.object_hook, *args, **kwargs
            )

        def object_hook(self, obj):

            """
            Executed on every object.
            """

            if "_type" not in obj:
                return obj

            if obj["_type"] in Object.types:
                return Object.types[obj["_type"]].decode(obj)
            else:
                return obj

    ## --- Static Variables --- ##

    types = {}

    ## --- Static Functions --- ##

    @staticmethod
    def register(t):
        if type(t) != type(Object):
            raise TypeError(
                "Cannot register '" + type(t).__name__ + "' as a serializable type."
            )

        Object.types[t.__name__] = t

    ## --- Serialization --- ##

    def encode(self):

        """
        Serialize the object to a json string.
        """

        return json.dumps(
            {"_type": type(self).__name__, **self.__dict__}, cls=Object.Encoder
        )

    @staticmethod
    def decode(j):

        """
        Deserialize the object from a string or json.
        """

        if isinstance(j, str):
            j = json.loads(j, cls=Object.Decoder)

        o = j
        if isinstance(j, dict):
            o = Object.types[j.pop("_type", None)]()

            for k in j:
                setattr(o, k, j[k])

        return o

    ## --- Data Model functions --- #

    def __eq__(self, other):

        if type(self) != type(other):
            return False

        return self.__dict__ == other.__dict__


Object.register(Object)
