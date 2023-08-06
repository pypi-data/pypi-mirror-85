# coding=utf-8

from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Random import get_random_bytes

from typing import Tuple
from base64 import b64encode, b64decode
from io import UnsupportedOperation
from os import path, remove


class SecureBox(object):
    """SecureBox class for write and read SecureBox's boxes."""

    FILE_SEPARATOR = '.'
    ENCODING = 'utf-8'

    def __init__(self, file: str, password: str, fast_key_derivation: bool = False):
        """SecureBox constructor.

        :param file: SecureBox's filename.
        :type file: str
        :param password: SecureBox's password.
        :type password: str
        :param fast_key_derivation: Enable fast key derivation mode.
        :type fast_key_derivation: bool
        :return: SecureBox's instance.
        """
        if file is None or (not isinstance(file, str)):
            raise Exception('file must be a filename')
        self._file = file
        self._salt = None
        if path.exists(self._file):
            with open(self._file, 'r', encoding=self.ENCODING) as file:
                self._salt, _, _, _ = self.__unzip_file_data(file.read())
        self._fast_key_derivation = fast_key_derivation
        self._key = self.__derive_key(password)

    def __unzip_file_data(self, file_data: str) -> Tuple[bytes, bytes, bytes, bytes]:
        """Unzip file data to salt, nonce, MAC tag and content.

        :param file_data: File data.
        :type file_data: str
        :return: Tuple of (Salt, nonce, MAC tag and content).
        """
        try:
            salt, nonce, tag, body = file_data.split(self.FILE_SEPARATOR)
        except UnsupportedOperation:
            raise Exception(f'Impossible to read: {self._file}')
        if not salt:
            raise Exception('salt not found')
        if not nonce:
            raise Exception('nonce not found')
        if not tag:
            raise Exception('tag not found')
        if not body:
            raise Exception('body not found')
        return b64decode(salt), b64decode(nonce), b64decode(tag), b64decode(body)

    def __derive_key(self, password: str):
        """Derive key from passed password (uses 'scrypt').

        :param password: Password.
        :type password: str
        :return: Derived key.
        """
        if password is None or (not isinstance(password, str) or (not password)):
            raise Exception('password param must be non empty string')
        if self._salt is None:
            self._salt = get_random_bytes(16)
        return scrypt(password, self._salt, 32, N=2 ** 14 if self._fast_key_derivation else 2 ** 20, r=8, p=1)

    def delete(self) -> None:
        """Delete the SecureBox file.
        """
        remove(self._file)

    def read(self) -> bytes:
        """Read SecureBox file data.

        :return: SecureBox file data (bytes).
        """
        with open(self._file, 'r', encoding=self.ENCODING) as file:
            file_data = file.read()
            _, nonce, tag, body = self.__unzip_file_data(file_data)

            cipher = AES.new(self._key, AES.MODE_OCB, nonce=nonce)
            cipher.update(self._key + cipher.nonce)
            return cipher.decrypt_and_verify(body, tag)

    def overwrite(self, data: bytes) -> None:
        """Overwrite the SecureBox file data with passed data.

        :param data: Data to write.
        :type data: bytes
        """
        if data is None:
            return
        with open(self._file, 'w', encoding=self.ENCODING) as file:
            cipher = AES.new(self._key, AES.MODE_OCB)
            cipher.update(self._key + cipher.nonce)
            ciphertext, tag = cipher.encrypt_and_digest(data)

            file.write(f'{b64encode(self._salt).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(cipher.nonce).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(tag).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(ciphertext).decode(encoding=self.ENCODING)}')

    def append(self, data: bytes) -> None:
        """Append passed data to the SecureBox file.

        :param data: Data to append.
        :type data: bytes
        """
        if data is None:
            return
        plaintext = None
        if not path.exists(self._file):
            with open(self._file, 'x', encoding=self.ENCODING):
                pass
        else:
            plaintext = self.read()
        with open(self._file, 'r+', encoding=self.ENCODING) as file:
            cipher = AES.new(self._key, AES.MODE_OCB)
            cipher.update(self._key + cipher.nonce)
            ciphertext, tag = cipher.encrypt_and_digest(plaintext + data if plaintext else data)

            file.truncate(0)
            file.write(f'{b64encode(self._salt).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(cipher.nonce).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(tag).decode(encoding=self.ENCODING)}{self.FILE_SEPARATOR}'
                       f'{b64encode(ciphertext).decode(encoding=self.ENCODING)}')
