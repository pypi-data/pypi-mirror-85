from samson.encoding.pem import PEMEncodable

class X509PublicKeyBase(PEMEncodable):
    DEFAULT_MARKER = 'PUBLIC KEY'
    DEFAULT_PEM = True
    USE_RFC_4716 = False

    def __init__(self, key: object, **kwargs):
        self.key = key
