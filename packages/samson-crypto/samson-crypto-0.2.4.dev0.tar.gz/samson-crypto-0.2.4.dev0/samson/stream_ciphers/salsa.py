from samson.utilities.manipulation import left_rotate, get_blocks
from samson.utilities.bytes import Bytes
from samson.core.primitives import StreamCipher, Primitive
from samson.core.metadata import SizeType, SizeSpec, EphemeralSpec, EphemeralType, ConstructionType, FrequencyType
from samson.ace.decorators import register_primitive
from copy import deepcopy
import math


def QUARTER_ROUND(a: int, b: int, c: int, d: int) -> (int, int, int, int):
    """
    Performs a quarter round of Salsa.

    Parameters:
        a (int): Salsa state variable.
        b (int): Salsa state variable.
        c (int): Salsa state variable.
        d (int): Salsa state variable.
    
    Returns:
        (int, int, int, int): New values for (a, b, c, d).
    """
    b = (b ^ left_rotate((a + d) & 0xFFFFFFFF,  7))
    c = (c ^ left_rotate((b + a) & 0xFFFFFFFF,  9))
    d = (d ^ left_rotate((c + b) & 0xFFFFFFFF, 13))
    a = (a ^ left_rotate((d + c) & 0xFFFFFFFF, 18))
    return a, b, c, d


@register_primitive()
class Salsa(StreamCipher):
    """
    Salsa stream cipher

    Add-rotate-xor (ARX) structure.

    https://en.wikipedia.org/wiki/Salsa20
    """

    CONSTRUCTION_TYPES = [ConstructionType.ADD_ROTATE_XOR]
    EPHEMERAL          = EphemeralSpec(ephemeral_type=EphemeralType.NONCE, size=SizeSpec(size_type=SizeType.SINGLE, sizes=96))
    USAGE_FREQUENCY    = FrequencyType.UNUSUAL

    def __init__(self, key: bytes, nonce: bytes, rounds: int=20, constant: bytes=b"expand 32-byte k"):
        """
        Parameters:
            key      (bytes): Key (128 or 256 bits).
            nonce    (bytes): Nonce (8 bytes).
            rounds     (int): Number of rounds to perform.
            constant (bytes): Constant used in generating the keystream (16 bytes).
        """
        Primitive.__init__(self)

        # If key is 80 bits, zero pad it (https://cr.yp.to/snuffle/salsafamily-20071225.pdf, 4.1)
        if len(key) == 10:
            key = Bytes.wrap(key).zfill(16)

        # If key is 128 bits, just repeat it
        if len(key) == 16:
            key += key

        self.key = key
        self.nonce = nonce
        self.rounds = rounds
        self.constant = constant
        self.counter = 0




    def full_round(self, block_num: int, state: list=None) -> Bytes:
        """
        Performs a full round of Salsa.

        Parameters:
            block_num (int): Current block number.
        
        Returns:
            Bytes: Keystream block.
        """
        ctr_bytes = int.to_bytes(block_num, 8, 'little')

        cons_blocks  = [int.from_bytes(block, 'little') for block in get_blocks(self.constant, 4)]
        key_blocks   = [int.from_bytes(block, 'little') for block in get_blocks(self.key, 4)]
        ctr_blocks   = [int.from_bytes(block, 'little') for block in get_blocks(ctr_bytes, 4)]
        nonce_blocks = [int.from_bytes(block, 'little') for block in get_blocks(self.nonce, 4)]

        x = state or [
            cons_blocks[0],  *key_blocks[:4],
            cons_blocks[1],  *nonce_blocks,
            *ctr_blocks,     cons_blocks[2],
            *key_blocks[4:], cons_blocks[3]
        ]

        x = deepcopy(x)
        tmp = deepcopy(x)

        for _ in range(self.rounds // 2):
            # Odd round
            x[ 0], x[ 4], x[ 8], x[12] = QUARTER_ROUND(x[ 0], x[ 4], x[ 8], x[12])
            x[ 5], x[ 9], x[13], x[ 1] = QUARTER_ROUND(x[ 5], x[ 9], x[13], x[ 1])
            x[10], x[14], x[ 2], x[ 6] = QUARTER_ROUND(x[10], x[14], x[ 2], x[ 6])
            x[15], x[ 3], x[ 7], x[11] = QUARTER_ROUND(x[15], x[ 3], x[ 7], x[11])

            # Even round
            x[ 0], x[ 1], x[ 2], x[ 3] = QUARTER_ROUND(x[ 0], x[ 1], x[ 2], x[ 3])
            x[ 5], x[ 6], x[ 7], x[ 4] = QUARTER_ROUND(x[ 5], x[ 6], x[ 7], x[ 4])
            x[10], x[11], x[ 8], x[ 9] = QUARTER_ROUND(x[10], x[11], x[ 8], x[ 9])
            x[15], x[12], x[13], x[14] = QUARTER_ROUND(x[15], x[12], x[13], x[14])

        for i in range(16):
            x[i] += tmp[i]

        return Bytes(b''.join([int.to_bytes(state_int & 0xFFFFFFFF, 4, 'little') for state_int in x]), byteorder='little')




    def yield_state(self, start_chunk: int=0, num_chunks: int=1, state: list=None):
        """
        Generates `num_chunks` chunks of keystream starting from `start_chunk`.

        Parameters:
            num_chunks  (int): Desired number of 64-byte keystream chunks.
            start_chunk (int): Chunk number to start at.
            state      (list): Custom state to be directly injected.
        
        Returns:
            generator: Keystream chunks.
        """
        for iteration in range(start_chunk, start_chunk + num_chunks):
            yield self.full_round(iteration, state=state)



    def generate(self, length: int) -> Bytes:
        """
        Generates `length` of keystream.

        Parameters:
            length (int): Desired length of keystream in bytes.
        
        Returns:
            Bytes: Keystream.
        """
        num_chunks  = math.ceil(length / 64)
        start_chunk = self.counter // 64

        counter_mod = self.counter % 64

        if counter_mod:
            num_chunks += 1

        keystream = sum(list(self.yield_state(start_chunk=start_chunk, num_chunks=num_chunks)))[counter_mod:counter_mod+length]
        self.counter += length

        return keystream
