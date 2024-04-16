import io
import struct

from .serializable import ConstructableRegistry
from .types import Instant

LONG_MIN_VALUE = -(2**63)
INTEGER_MIN_VALUE = -(2**31)


class DataInputStream:
    def __init__(self, stream):
        self.stream = stream
        self.size = stream.seek(0, io.SEEK_END)
        stream.seek(0, io.SEEK_SET)

    def read_boolean(self):
        return struct.unpack("?", self.stream.read(1))[0]

    def read_byte(self):
        return struct.unpack("b", self.stream.read(1))[0]

    def read_fully(self, numBytes):
        ret = self.stream.read(numBytes)
        assert len(ret) == numBytes
        return ret

    def available(self):
        return self.stream.tell() < self.size

    def read_unsigned_byte(self):
        return struct.unpack("B", self.stream.read(1))[0]

    def read_char(self):
        return chr(struct.unpack(">H", self.stream.read(2))[0])

    def read_double(self):
        return struct.unpack(">d", self.stream.read(8))[0]

    def read_float(self):
        return struct.unpack(">f", self.stream.read(4))[0]

    def read_short(self):
        return struct.unpack(">h", self.stream.read(2))[0]

    def read_unsigned_short(self):
        return struct.unpack(">H", self.stream.read(2))[0]

    def read_long(self):
        return struct.unpack(">q", self.stream.read(8))[0]

    def read_unsigned_long(self):
        return struct.unpack(">Q", self.stream.read(8))[0]

    def read_utf(self):
        utf_length = struct.unpack(">H", self.stream.read(2))[0]
        return self.stream.read(utf_length)

    def read_int(self):
        return struct.unpack(">i", self.stream.read(4))[0]

    def read_byte_array(self, maxLength, readChecksum=False):
        l = self.read_int()
        if l < 0:
            return
        if readChecksum:
            checksum = self.read_int()
            assert (
                checksum == 101 - l
            ), "SerializableDataInputStream tried to create array of length with wrong checksum."
        assert l <= maxLength
        return self.read_fully(l)

    def read_long_array(self):
        l = self.read_int()
        if l < 0:
            return []

        result = []
        i = 0
        while i < l:
            result.append(self.read_long())
            i += 1

        return l, result

    def read_int_array(self):
        l = self.read_int()
        if l < 0:
            return []

        result = []
        i = 0
        while i < l:
            result.append(self.read_int())
            i += 1

        return l, result

    def read_instant(self):
        epochSecond = self.read_long()
        if epochSecond == LONG_MIN_VALUE:
            return
        nanos = self.read_long()
        assert nanos >= 0 and nanos <= 999999999, "Instant.nanosecond is not within the allowed range!"
        return Instant(epochSecond, nanos)


class SerializableDataInputStream(DataInputStream):
    def validateVersion(self, object, version):
        # print("version: ", version)
        # print("object.CLASS_VERSION: ", object.CLASS_VERSION)
        assert version >= 1 and version <= object.CLASS_VERSION, "Invalid version"

    def validateFlag(self, object):
        # for debug build only
        pass

    def readSerializable(self, readClassId, serializableConstructor):
        classId = None
        if readClassId:
            classId = self.read_unsigned_long()
            if classId == LONG_MIN_VALUE:
                return
        version = self.read_int()

        if version == INTEGER_MIN_VALUE:
            return
        if readClassId:
            serializableConstructor = ConstructableRegistry.createObject(classId)
        selfSerializable = serializableConstructor()
        self.validateVersion(selfSerializable, version)
        selfSerializable.deserialize(self, version)
        self.validateFlag(selfSerializable)
        return selfSerializable

    def readSerializableIterableWithSize(self, size, readClassId, serializableConstructor, callback):
        if size == 0:
            return
        allSameClass = self.read_boolean()
        classIdVersionRead = False
        version = None
        classId = None
        for i in range(size):
            if not allSameClass:
                callback(self.readSerializable(readClassId, serializableConstructor))
            else:
                isNull = self.read_boolean()
                if isNull:
                    callback(None)
                else:
                    if not classIdVersionRead:
                        if readClassId:
                            classId = self.read_long()
                        version = self.read_int()
                        classIdVersionRead = True
                    selfSerializable = serializableConstructor()
                    selfSerializable.deserialize(self, version)
                    callback(selfSerializable)

    def readSerializableList(self, maxListSize, readClassId, serializableConstructor):
        length = self.read_int()
        if length == -1:
            return
        assert length <= maxListSize
        list_ = []
        if length == 0:
            return list_
        self.readSerializableIterableWithSize(length, readClassId, serializableConstructor, list_.append)
        return list_

    def readSerializableArray(self, maxListSize, readClassId, serializableConstructor):
        return self.readSerializableList(maxListSize, readClassId, serializableConstructor)
