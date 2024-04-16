import datetime
import struct
from collections import namedtuple


class Instant:
    def __init__(self, sec, nsec):
        self.sec = sec
        self.nsec = nsec

    @staticmethod
    def read(dis):
        return Instant(dis.read_long(), dis.read_long())

    def to_bytes(self):
        return struct.pack(">qq", self.sec, self.nsec)

    def to_nanos(self):
        return 1000000000 * self.sec + self.nsec

    def to_seconds(self):
        return self.sec + round(self.nsec / 10**9, 6)

    def __str__(self):
        # return '%d.%.9d' % (self.sec, self.nsec)
        return datetime.datetime.utcfromtimestamp(self.to_seconds()).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


DigestType = namedtuple("DigestType", "algorithmName provider outputLength")
digestTypes = {
    1493139739: DigestType("SHA-384", "SUN", 48),
    -1882633858: DigestType("SHA-512", "SUN", 64),
}


SignatureType = namedtuple("SignatureType", "signingAlgorithm keyAlgorithm provider signatureLength")
signatureTypes = {
    0: SignatureType("NONEwithED25519", "ED25519", "", 64),
    1: SignatureType("SHA384withRSA", "RSA", "SunRsaSign", 384),
    2: SignatureType("SHA384withECDSA", "EC", "SunEC", 104),
}
