import time
import base64
import binascii
import string
from decimal import Decimal

from . import strutils
from . import randomutils
from . import aesutils
from .aesutils import get_md5_key as md5_key
from .aesutils import get_mysql_aes_key as mysql_aes_key
from .aesutils import get_sha1prng_key as sha1prng_key
from .aesutils import padding_ansix923 as aes_padding_ansix923
from .aesutils import padding_iso10126 as aes_padding_iso10126
from .aesutils import padding_pkcs5 as aes_padding_pkcs5


class DecryptFailed(RuntimeError):
    pass

class S12CipherCore(object):

    def __init__(self, password):
        self.password = password
        self.s12_encode_map = self.get_s12_encode_map()
        self.s12_encode_bytes = self.get_s12_encode_bytes()
        self.s12_decode_bytes = self.get_s12_decode_bytes()

    def get_s12_encode_map(self):
        v = randomutils.Random(self.password).get_bytes(256)
        values = list(range(256))
        delta = 0
        for index in range(256):
            delta += v[index]
            values[index] += delta
        return values

    def get_s12_encode_bytes(self):
        encode_map = self.s12_encode_map
        encode_bytes = {}
        for code in range(256):
            value = encode_map[code]
            high = value // 256
            low = value % 256
            encode_bytes[bytes([code])] = bytes([high, low])
        return encode_bytes

    def get_s12_decode_bytes(self):
        encode_map = self.s12_encode_map
        decode_bytes = {}
        for code in range(256):
            value = encode_map[code]
            high = value // 256
            low = value % 256
            decode_bytes[bytes([high, low])] = bytes([code])
        return decode_bytes

    def encrypt(self, data, **kwargs):
        data = strutils.force_bytes(data)
        encode_bytes = self.s12_encode_bytes
        return b"".join([encode_bytes[bytes([code])] for code in data])

    def decrypt(self, data, **kwargs):
        result = b''
        decode_bytes = self.s12_decode_bytes
        for start in range(0, len(data), 2):
            result += decode_bytes[data[start: start + 2]]
        return result

def s12_encrypt(data, password):
    cipher = S12CipherCore(password)
    return cipher.encrypt(data)

def s12_decrypt(data, password):
    cipher = S12CipherCore(password)
    return cipher.decrypt(data)

class MappingCipherBase(object):
    def __init__(self, password):
        self.password = password
        self.randomGenerator = randomutils.Random(self.password)
        self.seeds = self.get_seeds()
        self.encrypt_mapping = self.get_encrypt_mapping()
        self.decrypt_mapping = self.get_decrypt_mapping()

    def get_seeds(self):
        raise NotImplementedError()

    def get_encrypt_mapping(self):
        mapping = {}
        for i in range(256):
            mapping[bytes([i])] = self.seeds[i]
        return mapping
    
    def get_decrypt_mapping(self):
        mapping = {}
        for i in range(256):
            mapping[self.seeds[i]] = bytes([i])
        return mapping
    
    def encrypt(self, data, **kwargs):
        if data is None:
            return None
        result = b""
        data = strutils.force_bytes(data)
        for c in data:
            result += self.encrypt_mapping[bytes([c])]
        return result
    
    def decrypt(self, data, **kwargs):
        if data is None:
            return None
        result = b""
        data_length = len(data)
        max_seed_length = max([len(x) for x in self.decrypt_mapping.keys()])
        start = 0
        while start < data_length:
            found = False
            for seed_length in range(1, max_seed_length+1):
                seed = data[start: start+seed_length]
                if seed in self.decrypt_mapping:
                    result += self.decrypt_mapping[seed]
                    start += seed_length
                    found = True
                    break
            if not found:
                raise DecryptFailed()
        return result

class S1CipherCore(MappingCipherBase):
    def get_seeds(self):
        seeds = list(range(256))
        self.randomGenerator.shuffle(seeds)
        return [bytes([x]) for x in seeds]

class S2CipherCore(MappingCipherBase):
    def get_seeds(self):
        letters = string.ascii_lowercase
        seeds = set()
        for a in letters:
            for b in letters:
                seeds.add(a+b)
        seeds = list(seeds)
        self.randomGenerator.shuffle(seeds)
        seeds = [x.encode() for x in seeds[:256]]
        return seeds

class IvCipherCore(object):
    def __init__(self, password):
        self.password = password
        self.iv_params = self.get_iv_params()

    def get_iv_params(self):
        gen = randomutils.Random(self.password)
        n = gen.randint(1024, 9999)
        iv = [gen.randint(1, 100) for _ in range(n)]
        return n, iv

    def encrypt(self, number, **kwargs):
        number = strutils.force_int(number)
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
        s = sum(iv)
        a = number // n
        b = number % n
        r = a * s + sum(iv[:b])
        if flag:
            r = -1 * r
        return r

    def decrypt(self, number, **kwargs):
        number = strutils.force_int(number)
        flag = False
        if number < 0:
            number = -1 * number
            flag = True
        n, iv = self.iv_params
        s = sum(iv)
        a = number // s
        t = s * a
        if t == number:
            r = a * n
        else:
            for delta in range(n):
                t += iv[delta]
                if t == number:
                    r = a * n + delta + 1
                    break
            if t != number:
                raise DecryptFailed("iv_decrypt failed: number={}".format(number))
        if flag:
            r = -1 * r
        return r

def iv_encrypt(number, password):
    cipher = IvCipherCore(password)
    return cipher.encrypt(number)

def iv_decrypt(number, password):
    cipher = IvCipherCore(password)
    return cipher.decrypt(number)

class IvfCipherCore(IvCipherCore):

    def __init__(self, password, int_digits=12, float_digits=4):
        super().__init__(password)
        self.int_digits = int_digits
        self.float_digits = float_digits
        self.module = 10 ** (float_digits * 2)
        self.max_value_length = float_digits * 2 + self.int_digits + 2
        self.max = 10 ** self.max_value_length - 1
        self.value_template = "{:0%dd}" % self.max_value_length

    def encrypt(self, number, **kwargs):
        number = int(number * self.module)
        number = super().encrypt(number)
        if number >= 0:
            return "+" + self.value_template.format(number)
        else:
            return "*" + self.value_template.format(self.max - abs(number))

    def decrypt(self, number, **kwargs):
        sign = number[0]
        number = int(number[1:])
        if sign == "*":
            number = self.max - number
        number = super().decrypt(number)
        number = round(number / self.module, self.float_digits)
        if self.float_digits == 0:
            number = int(number)
        if sign == "*":
            return -1 * number
        else:
            return number

class EncoderBase(object):

    def encode(self, data: bytes) -> str:
        raise NotImplementedError()

    def decode(self, data: str) -> bytes:
        raise NotImplementedError()

class RawDataEncoder(EncoderBase):

    def encode(self, data: bytes) -> bytes:
        return data
    
    def decode(self, data: bytes) -> bytes:
        return data

class HexlifyEncoder(EncoderBase):

    def encode(self, data: bytes) -> str:
        if data is None:
            return None
        return binascii.hexlify(data).decode()

    def decode(self, data: str) -> bytes:
        if data is None:
            return None
        return binascii.unhexlify(data.encode("utf-8"))

class Base64Encoder(EncoderBase):

    def encode(self, data: bytes) -> str:
        if data is None:
            return None
        return strutils.join_lines(base64.encodebytes(data)).decode()

    def decode(self, data: str) -> bytes:
        if data is None:
            return None
        return base64.decodebytes(data.encode("utf-8"))

class SafeBase64Encoder(EncoderBase):

    def encode(self, data: bytes) -> str:
        if data is None:
            return None
        return strutils.join_lines(base64.urlsafe_b64encode(data)).decode()

    def decode(self, data: str) -> bytes:
        if data is None:
            return None
        return base64.urlsafe_b64decode(data.encode("utf-8"))

class Utf8Encoder(EncoderBase):
    
    def encode(self, data: bytes) -> str:
        if not data:
            return None
        return data.decode("utf-8")

    def decode(self, data: str) -> bytes:
        if not data:
            return None
        return data.encode("utf-8")


class CipherBase(object):

    def get_defaults(self):
        if hasattr(self, "defaults"):
            return getattr(self, "defaults")
        else:
            return {}

    def __init__(self, **kwargs):
        params = {}
        params.update(self.defaults)
        params.update(kwargs)
        self.password = params.get("password", None)
        self.encrypt_kwargs = params.get("encrypt_kwargs", {})
        self.decrypt_kwargs = params.get("decrypt_kwargs", {})
        self.kwargs = params.get("kwargs", {})
        if self.password:
            self.kwargs.update({"password": self.password})
        self.result_encoder = params["result_encoder"]
        self.force_text = params.get("force_text", False)
        self.text_encoding = params.get("text_encoding", "utf-8")
        self.cipher_core_class = params.get("cipher_core", None)
        if self.cipher_core_class:
            self.cipher_instance = self.cipher_core_class(**self.kwargs)
            self._encrypt = self.cipher_instance.encrypt
            self._decrypt = self.cipher_instance.decrypt
        else:
            self._encrypt = params["encrypt"]
            self._decrypt = params["decrypt"]

    def encrypt(self, data):
        if data is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.encrypt_kwargs)
        data = strutils.force_bytes(data, self.text_encoding)
        encrypted_data = self._encrypt(data, **params)
        return self.result_encoder.encode(encrypted_data)

    def decrypt(self, text):
        if text is None:
            return None
        params = {}
        params.update(self.kwargs)
        params.update(self.decrypt_kwargs)
        data = self.result_encoder.decode(text)
        decrypted_data = self._decrypt(data, **params)
        if self.force_text:
            return strutils.force_text(decrypted_data, self.text_encoding)
        else:
            return decrypted_data

class AesCipher(CipherBase):
    
    defaults = {
        "result_encoder": RawDataEncoder(),
        "encrypt": aesutils.encrypt,
        "decrypt": aesutils.decrypt,
    }

class MysqlAesCipher(CipherBase):
    
    defaults = {
        "result_encoder": RawDataEncoder(),
        "encrypt": aesutils.encrypt,
        "decrypt": aesutils.decrypt,
        "kwargs": {
            "key": mysql_aes_key
        }
    }

class S12Cipher(CipherBase):

    defaults = {
        "result_encoder": RawDataEncoder(),
        "cipher_core": S12CipherCore,
    }

class IvCipher(CipherBase):

    defaults = {
        "result_encoder": RawDataEncoder(),
        "cipher_core": IvCipherCore,
    }

class IvfCipher(CipherBase):

    defaults = {
        "result_encoder": RawDataEncoder(),
        "cipher_core": IvfCipherCore,
        "kwargs": {
            "int_digits": 12,
            "float_digits": 4,
        }
    }

class S1Cipher(CipherBase):

    defaults = {
        "result_encoder": RawDataEncoder(),
        "cipher_core": S1CipherCore,
    }

class S2Cipher(CipherBase):

    defaults = {
        "result_encoder": Utf8Encoder(),
        "cipher_core": S2CipherCore,
    }
