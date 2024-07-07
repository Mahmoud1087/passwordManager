from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
import base64
import os


def decoding(input):
    return base64.decodebytes(input.encode("ascii"))


encryption_key = os.environ.get("ENCRYPTION_KEY")
KEY = decoding(encryption_key)


def encoding(input):
    encoded = base64.b64encode(input)
    encoded = encoded.decode("UTF-8")
    return encoded


def encrypt_data(plaintext, key=KEY):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode("ascii"), AES.block_size))
    return encoding(ciphertext)


def decrypt_data(encryption, key=KEY):
    ciphertext = decoding(encryption)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(ciphertext), AES.block_size)
    decrypted_text = decrypted_text.decode("UTF-8")
    return decrypted_text
