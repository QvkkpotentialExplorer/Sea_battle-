import gostcrypto
import base64

key = bytearray([
    0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    0xfe, 0xdc, 0xba, 0x98, 0x76, 0x54, 0x32, 0x10, 0x01, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef,
])

init_vect = bytearray([
    0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff, 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
])


def b32decrypt(data: str) -> str:
    global init_vect, key

    plain_text = bytearray(base64.b32decode(data))
    cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                           key,
                                           gostcrypto.gostcipher.MODE_CFB,
                                           init_vect=init_vect)

    decrypt_text = cipher_obj.decrypt(plain_text)

    return decrypt_text.replace(b'\x00', b'').decode()


def b32encrypt(data: str) -> str:
    global init_vect, key

    plain_text = bytearray(str(data).encode())
    cipher_obj = gostcrypto.gostcipher.new('kuznechik',
                                           key,
                                           gostcrypto.gostcipher.MODE_CFB,
                                           init_vect=init_vect)

    cipher_text = cipher_obj.encrypt(plain_text)

    return base64.b32encode(cipher_text).decode()