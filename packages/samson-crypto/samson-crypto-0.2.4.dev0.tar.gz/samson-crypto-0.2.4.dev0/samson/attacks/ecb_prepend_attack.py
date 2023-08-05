from samson.utilities.manipulation import get_blocks
from samson.utilities.bytes import Bytes
from samson.oracles.chosen_plaintext_oracle import ChosenPlaintextOracle
from samson.utilities.runtime import RUNTIME
import struct

import logging
log = logging.getLogger(__name__)

class ECBPrependAttack(object):
    """
    Performs a plaintext recovery attack.

    By prepending data to the secret, we can take advantage of ECB's statelessness and iteratively build
    ciphertext blocks that match the secret's ciphertext blocks.

    Conditions:
        * ECB is being used
        * The user has access to an oracle that accepts arbitrary plaintext and returns the ciphertext
        * The user's input is prepended to the secret plaintext
    """

    def __init__(self, oracle: ChosenPlaintextOracle):
        """
        Parameters:
            oracle (ChosenPlaintextOracle): An oracle that takes in plaintext and returns the ciphertext.
        """
        self.oracle = oracle


    @RUNTIME.report
    def execute(self) -> Bytes:
        """
        Executes the attack.

        Parameters:
            unpad (bool): Whether or not to PKCS7 unpad the result.
        
        Returns:
            Bytes: The recovered plaintext.
        """
        baseline   = len(self.oracle.request(b''))
        block_size = self.oracle.test_io_relation()['block_size']

        plaintexts = []
        for curr_block in RUNTIME.report_progress(range(baseline // block_size), unit='blocks'):
            log.debug(f"Starting iteration {curr_block}")

            plaintext = b''
            for curr_byte in RUNTIME.report_progress(range(block_size), unit='bytes'):
                if curr_block == 0:
                    payload = ('A' * (block_size - (curr_byte + 1))).encode()
                else:
                    payload = plaintexts[-1][curr_byte + 1:]

                one_byte_short = get_blocks(self.oracle.request(payload), block_size=block_size)[curr_block]

                for i in range(256):
                    curr_byte  = struct.pack('B', i)
                    ciphertext = self.oracle.request(payload + plaintext + curr_byte)

                    # We're always editing the first block to look like block 'curr_block'
                    if get_blocks(ciphertext, block_size=block_size)[0] == one_byte_short:
                        plaintext += curr_byte
                        break

            plaintexts.append(plaintext)
        return Bytes(b''.join(plaintexts))
