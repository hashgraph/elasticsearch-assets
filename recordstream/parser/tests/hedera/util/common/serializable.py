import hashlib
import io
import struct

from .types import Instant, digestTypes, signatureTypes

MAX_SIG_LENGTH = 384
MAX_TRANSACTION_COUNT_PER_EVENT = 245_760
TRANSACTION_MAX_BYTES = 6_144

MAX_RECORD_LENGTH = 64 * 1024
MAX_TRANSACTION_LENGTH = 64 * 1024


class ConstructableRegistry:
    class_map = {}

    # decorator function, registers the class with a static CLASS_ID value
    @staticmethod
    def register(cls):
        assert hasattr(cls, "CLASS_ID")
        assert cls.CLASS_ID not in ConstructableRegistry.class_map
        ConstructableRegistry.class_map[cls.CLASS_ID] = cls
        return cls

    # returns the class with the given class ID
    @staticmethod
    def createObject(classId):
        assert classId in ConstructableRegistry.class_map, "Class ID %s not found" % hex(classId)
        return ConstructableRegistry.class_map[classId]


@ConstructableRegistry.register
class Hash:
    CLASS_ID = 0xF422DA83A251741E
    CLASS_VERSION = 1

    def __init__(self):
        self.digestType = None
        self.hashValue = None

    def deserialize(self, dis, version=None):
        digestType = digestTypes[dis.read_int()]
        hashValue = dis.read_byte_array(digestType.outputLength)
        assert any(b != 0 for b in hashValue), "Hash creation failed, hash is array of zeroes"
        self.digestType = digestType
        self.value = hashValue

        self.struct = {
            "digestType": self.digestType.algorithmName,
            "value": self.value.hex(),
        }


#  THIS CLASS IS UNTESTED
class Signature:
    def __init__(
        self,
        contents,
        signature_offset,
        signature_length,
        expanded_public_key,
        public_key_offset,
        public_key_length,
        message_offset,
        message_length,
        signature_type,
    ):

        assert contents != None and len(contents) != 0

        public_key_source = expanded_public_key if expanded_public_key is not None else contents

        assert signature_offset >= 0 and signature_offset <= len(contents)
        assert (
            signature_length >= 0
            and signature_length <= len(contents)
            and signature_length + signature_offset <= len(contents)
        )

        assert public_key_offset >= 0 and public_key_offset <= len(public_key_source)
        assert (
            public_key_length >= 0
            and public_key_length <= len(public_key_source)
            and public_key_length + public_key_offset <= len(public_key_source)
        )

        assert message_offset >= 0 and message_offset <= len(contents)
        assert (
            message_length >= 0 and message_length <= len(contents) and message_length + message_offset <= len(contents)
        )

        self.contents = contents
        self.expanded_public_key = expanded_public_key

        self.signature_offset = signature_offset
        self.signature_length = signature_length

        self.public_key_offset = public_key_offset
        self.public_key_length = public_key_length

        self.message_offset = message_offset
        self.message_length = message_length

        self.signature_type = signatureTypes[signature_type]

        self.struct = {
            "contents": contents.hex(),
            "expandedPublicKey": expanded_public_key.hex(),
            "messageOffset": message_offset,
            "messageLength": message_length,
            "publicKeyOffset": public_key_offset,
            "publicKeyLength": public_key_length,
            "signatureOffset": signature_offset,
            "signatureLength": signature_length,
            "signatureType": signature_type.signingAlgorithm,
        }

    @staticmethod
    def deserialize(dis, byte_count):
        total_bytes = [7 * 4]

        # Read Signature Length w/ Simple Prime Number Checksum
        sig_len = dis.read_int()
        sig_checksum = dis.read_int()

        assert sig_len >= 0 and sig_checksum == (
            439 - sig_len
        ), "Signature.deserialize tried to create signature array of length %d"
        " with wrong checksum." % sig_len

        # Read Signature
        sig_type = signatureTypes[dis.read_int()]
        sig = dis.read_fully(sig_len)
        total_bytes[0] += len(sig)

        # Read Public Key Length w/ Simple Prime Number Checksum
        pk_len = dis.read_int()
        pk_checksum = dis.read_int()

        assert pk_len >= 0 and pk_checksum == (
            541 - pk_len
        ), "Signature.deserialize tried to create public key array of length %d"
        " with wrong checksum." % pk_len

        # Read Public Key
        if pk_len > 0:
            pk = dis.read_fully(pk_len)
            total_bytes[0] += len(pk)
        else:
            pk = b""

        # Read Message Length w/ Simple Prime Number Checksum
        msg_len = dis.read_int()
        msg_checksum = dis.read_int()

        assert msg_len >= 0 and msg_checksum == (647 - msg_len), (
            "Signature.deserialize tried to create message array of length %d with wrong checksum." % pk_len
        )

        # Read Message
        if msg_len > 0:
            msg = dis.read_fully(msg_len)
            total_bytes[0] += len(msg)
        else:
            msg = b""

        if byte_count is not None and len(byte_count) > 0:
            byte_count[0] += total_bytes[0]

        buffer = msg + pk + sig

        return Signature(
            buffer,
            len(msg) + len(pk),
            len(sig),
            None,
            len(msg),
            len(pk),
            0,
            len(msg),
            sig_type,
        )


@ConstructableRegistry.register
class Transaction:
    CLASS_ID = 0xA0EDA13E329FECCA
    CLASS_VERSION = 1

    def deserialize(self, dis, version, counts=None):
        if counts is None:
            counts = [0]
        total_bytes = [4 * 4 + 1]

        # Read Content Length w/ Simple Prime Number Checksum
        tx_len = dis.read_int()
        tx_checksum = dis.read_int()

        assert tx_len >= 0 and tx_checksum == (277 - tx_len), (
            "Transaction.deserialize tried to create contents array of length %d" " with wrong checksum."
        ) % tx_len
        assert tx_len <= TRANSACTION_MAX_BYTES, (
            "Transaction.deserialize tried to create contents array of length (%d) which is larger than "
            "maximum allowed size for a transaction (transactionMaxBytes = %d)"
        ) % (tx_len, TRANSACTION_MAX_BYTES)

        # Read Content
        system = dis.read_boolean()
        contents = dis.read_fully(tx_len)

        total_bytes[0] += len(contents)

        # Read Signature Length w/ Simple Prime Number Checksum
        sig_len = dis.read_int()
        sig_checksum = dis.read_int()

        assert sig_len >= 0 and sig_checksum == (353 - sig_len), (
            "Transaction.deserialize tried to create signature array of length %d" " with wrong checksum."
        ) % tx_len

        # Read Signatures
        sigs = []
        for i in range(sig_len):
            sigs.append(Signature.deserialize(dis, total_bytes))
        # add number of bytes in current Transaction into counts[0]
        counts[0] += total_bytes[0]

        self.contents = contents
        self.system = system
        self.signatures = sigs
        self.struct = {
            "contents": self.contents.hex(),
            "signatures": [s.struct for s in self.signatures],
            "system": self.system,
        }


@ConstructableRegistry.register
class TransactionV2:
    CLASS_ID = 0x9FF79186F4C4DB97
    CLASS_VERSION = 2

    def deserialize(self, dis, version, counts=None):
        if counts is None:
            counts = [0]
        total_bytes = [4 * 4 + 1]

        tx_len = dis.read_int()

        assert tx_len <= TRANSACTION_MAX_BYTES, (
            "Transaction.deserialize tried to create contents array of length (%d) which is larger than "
            "maximum allowed size for a transaction (transactionMaxBytes = %d)"
        ) % (tx_len, TRANSACTION_MAX_BYTES)

        # Read Content
        system = False
        contents = dis.read_fully(tx_len)

        total_bytes[0] += len(contents)
        counts[0] += total_bytes[0]

        self.contents = contents
        self.system = system

        self.struct = {"contents": self.contents.hex(), "system": self.system}


@ConstructableRegistry.register
class StateSignatureTransaction:
    CLASS_ID = 0xAF7024C653CAABF4
    CLASS_VERSION = 2

    def deserialize(self, dis, version):

        self.isFreeze = dis.read_boolean()
        self.signature = dis.read_byte_array(MAX_SIG_LENGTH)
        self.lastRoundReceived = dis.read_long()

        self.struct = {
            "isFreeze": self.isFreeze,
            "signature": self.signature.hex(),
            "lastRoundReceived": self.lastRoundReceived,
            "system": True,
        }


@ConstructableRegistry.register
class BitsPerSecondTransaction:
    CLASS_ID = 0x6922237D8F4DAC99
    CLASS_VERSION = 2

    def deserialize(self, dis, version):

        self.arrayLen, self.bitsPerSecond = dis.read_long_array()

        self.struct = {"contents": self.bitsPerSecond, "system": True}


@ConstructableRegistry.register
class PingTransaction:
    CLASS_ID = 0xE98D3E2C500A6647
    CLASS_VERSION = 2

    def deserialize(self, dis, version):

        self.arrayLen, self.pingValues = dis.read_int_array()

        self.struct = {"contents": self.pingValues, "system": True}


@ConstructableRegistry.register
class BaseEventHashedData:
    CLASS_ID = 0x21C2620E9B6A2243
    CLASS_VERSION = 2

    def checkUserTransactions(self):
        # todo
        pass

    def deserialize(
        self,
        dis,
        version,
        maxTransactionCount=MAX_TRANSACTION_COUNT_PER_EVENT,
        skipTransaction=False,
    ):
        start = dis.stream.tell()
        self.creatorId = dis.read_long()
        self.selfParentGen = dis.read_long()
        self.otherParentGen = dis.read_long()
        self.selfParentHash = dis.readSerializable(False, Hash)
        self.otherParentHash = dis.readSerializable(False, Hash)
        self.timeCreated = dis.read_instant()
        if version == 2:
            self.totalByteLength = dis.read_int()
            if skipTransaction:
                dis.read_fully(self.totalByteLength)
            else:
                self.transactions = dis.readSerializableArray(maxTransactionCount, True, Transaction)
        elif version == 1:
            self.transactions = dis.readSerializableArray(maxTransactionCount, False, Transaction)

        self.checkUserTransactions()
        end = dis.stream.tell()

        # calculate hash of parsed bytes
        dis.stream.seek(start, io.SEEK_SET)
        self.hash_bytes = struct.pack(
            ">QI",
            BaseEventHashedData.CLASS_ID,
            BaseEventHashedData.CLASS_VERSION,
        )
        self.hash_bytes += dis.read_fully(end - start)
        self.hash = hashlib.sha384(self.hash_bytes).hexdigest()

        self.struct = {
            "creatorId": self.creatorId,
            "selfParentGen": self.selfParentGen,
            "otherParentGen": self.otherParentGen,
            "selfParentHash": self.selfParentHash.struct,
            "otherParentHash": self.otherParentHash.struct,
            "timeCreated": str(self.timeCreated),
            "transactions": [s.struct for s in self.transactions],
            "hash": self.hash,
        }


@ConstructableRegistry.register
class BaseEventUnhashedData:
    CLASS_ID = 0x33CB9D4AE38C9E91
    CLASS_VERSION = 1

    def deserialize(self, dis, version=None):
        self.creatorSeq = dis.read_long()
        self.otherId = dis.read_long()
        self.otherSeq = dis.read_long()
        self.signature = dis.read_byte_array(MAX_SIG_LENGTH)

        self.struct = {
            "creatorSeq": self.creatorSeq,
            "otherId": self.otherId,
            "otherSeq": self.otherSeq,
            "signature": self.signature.hex(),
        }


@ConstructableRegistry.register
class ConsensusData:
    CLASS_ID = 0xDDF20B7CE114A711
    CLASS_VERSION = 2

    def deserialize(self, dis, version=None):
        self.generation = dis.read_long()
        self.roundCreated = dis.read_long()
        self.stale = dis.read_boolean()
        self.lastInRoundReceived = dis.read_boolean()
        self.consensusTimestamp = dis.read_instant()
        self.roundReceived = dis.read_long()
        self.consensusOrder = dis.read_long()

        self.struct = {
            "generation": self.generation,
            "roundCreated": self.roundCreated,
            "stale": self.stale,
            "lastInRoundReceived": self.lastInRoundReceived,
            "consensusTimestamp": str(self.consensusTimestamp),
            "roundReceived": self.roundReceived,
            "consensusOrder": self.consensusOrder,
        }


@ConstructableRegistry.register
class ConsensusEvent:
    CLASS_ID = 0xE250A9FBDCC4B1BA
    CLASS_VERSION = 1

    def deserialize(self, dis, version=None):
        self.baseEventHashedData = dis.readSerializable(False, BaseEventHashedData)
        self.baseEventUnhashedData = dis.readSerializable(False, BaseEventUnhashedData)
        self.consensusData = dis.readSerializable(False, ConsensusData)


class EventImpl:
    version = 1

    def __init__(self, consensusEvent):
        self.baseEventHashedData = consensusEvent.baseEventHashedData
        self.baseEventUnhashedData = consensusEvent.baseEventUnhashedData
        self.consensusData = consensusEvent.consensusData
        self.struct = {
            "baseEventHashedData": self.baseEventHashedData.struct,
            "baseEventUnhashedData": self.baseEventUnhashedData.struct,
            "consensusData": self.consensusData.struct,
        }


@ConstructableRegistry.register
class RecordStreamObject:
    CLASS_ID = 0xE370929BA5429D8B
    CLASS_VERSION = 1

    def deserialize(self, dis, version=None):
        self.transactionRecord = dis.read_byte_array(MAX_RECORD_LENGTH)
        self.transaction = dis.read_byte_array(MAX_TRANSACTION_LENGTH)
