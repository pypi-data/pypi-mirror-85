from samson.utilities.manipulation import get_blocks
from samson.utilities.bytes import Bytes
from samson.core.metadata import ConstructionType
from samson.core.primitives import Hash
from types import FunctionType
from copy import deepcopy


def md_pad(msg: bytes, fakeLen: int=None, byteorder: str='little', bit_size: int=64, encoded_size_length: int=None) -> bytes:
    length = fakeLen or len(msg)

    # Append the bit '1' to the message
    padding = b'\x80'
    byte_size = encoded_size_length or (bit_size // 8)

    # Append 0 <= k < 512 bits '0', so that the resulting message length (in bytes)
    # as congruent to 56 (mod 64)
    padding += b'\x00' * (((bit_size - byte_size) - (length + 1) % bit_size) % bit_size)

    # Append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    message_bit_length = length * 8

    padding += message_bit_length.to_bytes(byte_size, byteorder=byteorder)
    return msg + padding


class MerkleDamgardConstruction(Hash):
    """
    An iterative construction for building collision-resistant cryptographic hash functions from collision-resistant
    one-way compression functions. Used in MD4, MD5, SHA1, SHA2, RIPEMD, and more.
    """

    CONSTRUCTION_TYPES = [ConstructionType.MERKLE_DAMGARD]

    def __init__(self, initial_state: bytes, compression_func: FunctionType, digest_size: int, block_size: int=64, endianness: str='big', encoded_size_length: int=None):
        """
        Parameters:
            initial_state     (bytes): Bytes-like initial state that is the correct size for the underlying compression function.
            compression_func   (func): One-way compression function. Takes in the state and returns the next.
            digest_size         (int): Resulting digest size. Should be the same size as the `initial_state`.
            block_size          (int): Size of the internal state.
            endianness          (str): Endianess of the internal state.
            encoded_size_length (int): Size in bytes of encoded message length.
        """
        if not type(initial_state) is Bytes:
            initial_state = Bytes([_ for _ in initial_state])
        self.initial_state = initial_state

        # Allows for direct use of class and subclass overriding simultaneously
        if compression_func:
            self.compression_func = compression_func

        self.digest_size         = digest_size
        self.block_size          = block_size
        self.endianness          = endianness
        self.encoded_size_length = encoded_size_length


    def __reprdir__(self):
        return ['initial_state', 'compression_func', 'block_size']


    def pad_func(self, message: bytes) -> Bytes:
        """
        Pads the message with Merkle-Damgard padding.

        Parameters:
            message (bytes): Message to be padded.
        
        Returns:
            Bytes: Padded message.
        """
        return md_pad(message, None, self.endianness, bit_size=self.block_size, encoded_size_length=self.encoded_size_length)


    def yield_state(self, message: bytes) -> Bytes:
        """
        Yields the intermediate, hashed states of the `message`.

        Parameters:
            message (bytes): Message to be hashed.
        
        Returns:
            Bytes: Intermediate, hashed states.
        """
        state = self.initial_state

        for block in get_blocks(self.pad_func(message), self.block_size):
            state = self.compression_func(block, state)
            yield state


    def hash(self, message: bytes) -> Bytes:
        """
        Yields the final, hashed state of the `message`.

        Parameters:
            message (bytes): Message to be hashed.
        
        Returns:
            Bytes: Fully-hashed state.
        """
        final_state = list(self.yield_state(message))[-1]
        return final_state



    def length_extension(self, observed_output: bytes, message: bytes, bytes_to_append: bytes, secret_len: int) -> (Bytes, Bytes):
        """
        Performs a length-extension attack.

        Unaware developers may create a keyed-MAC using a Merkle-Damgard construction and prepending a
        secret key to the input. However, such schemes are susceptible to length-extension attacks where an
        attacker can forge a valid HMAC with an arbitrary, appended message.

        Parameters:
            observed_output (bytes): The observed, valid, hash output.
            message         (bytes): Message originally hashed.
            bytes_to_append (bytes): Bytes to append to the end.
            secret_len        (int): The length of the secret.
        
        Returns:
            (Bytes, Bytes): Result formatted as (crafted input, forged hash).
        """
        glue = md_pad(message, len(message) + secret_len, self.endianness, bit_size=self.block_size)[len(message):]

        fake_len = secret_len + len(message) + len(glue) + len(bytes_to_append)

        new_hash_obj = deepcopy(self)
        new_hash_obj.initial_state = observed_output
        new_hash_obj.pad_func = lambda msg: md_pad(msg, fake_len, self.endianness, bit_size=self.block_size)

        return Bytes(message + glue + bytes_to_append), new_hash_obj.hash(bytes_to_append)
