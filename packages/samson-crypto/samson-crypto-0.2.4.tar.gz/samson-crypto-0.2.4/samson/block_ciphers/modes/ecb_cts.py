from samson.utilities.bytes import Bytes
from samson.block_ciphers.modes.ecb import ECB
from samson.core.primitives import EncryptionAlg, BlockCipherMode, Primitive
from samson.ace.decorators import register_primitive

# https://en.wikipedia.org/wiki/Ciphertext_stealing
# CTS-3
@register_primitive()
class ECBCTS(BlockCipherMode):
    """Electronic codebook with ciphertext stealing block cipher mode."""

    def __init__(self, cipher: EncryptionAlg):
        """
        Parameters:
            cipher (EncryptionAlg): Instantiated encryption algorithm.
        """
        Primitive.__init__(self)
        self.underlying_mode = ECB(cipher)


    def encrypt(self, plaintext: bytes) -> Bytes:
        """
        Encrypts `plaintext`.

        Parameters:
            plaintext (bytes): Bytes-like object to be encrypted.
        
        Returns:
            Bytes: Resulting ciphertext.
        """
        plaintext  = Bytes.wrap(plaintext)
        block_size = self.underlying_mode.cipher.block_size
        pt_len     = len(plaintext)

        assert pt_len > block_size
        pt_chunks = plaintext.chunk(block_size, allow_partials=True)

        padding_len = (block_size - (pt_len % block_size)) % block_size
        ciphertext_chunks = self.underlying_mode.encrypt(sum(pt_chunks[:-1]), pad=False).chunk(block_size)
        padding = ciphertext_chunks[-1][-padding_len:][:padding_len]

        last_block = self.underlying_mode.encrypt(pt_chunks[-1] + padding, pad=False)

        return (sum(ciphertext_chunks[:-1]) + last_block + ciphertext_chunks[-1])[:pt_len]



    def decrypt(self, ciphertext: bytes) -> Bytes:
        """
        Decrypts `ciphertext`.

        Parameters:
            ciphertext (bytes): Bytes-like object to be decrypted.
        
        Returns:
            Bytes: Resulting plaintext.
        """
        ciphertext = Bytes.wrap(ciphertext)
        block_size = self.underlying_mode.cipher.block_size
        ct_len     = len(ciphertext)
        ct_chunks  = ciphertext.chunk(block_size, allow_partials=True)

        padding_len = (block_size - (ct_len % block_size)) % block_size
        D_n = self.underlying_mode.decrypt(ct_chunks[-2], unpad=False)
        padding = D_n[-padding_len:][:padding_len]

        return self.underlying_mode.decrypt(sum(ct_chunks[:-2]) + ct_chunks[-1] + padding + ct_chunks[-2], unpad=False)[:ct_len]
