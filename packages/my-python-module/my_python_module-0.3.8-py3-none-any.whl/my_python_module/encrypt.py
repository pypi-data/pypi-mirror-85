#!/usr/bin/env python
# -*-coding:utf-8-*-


"""
加密工具

- 加密salt 目标机器码
- 加密key 自定义
- 加密iv 目标机器码

存储的是 encrypted_msn 解密需要key 生成需要key

解密出msn之后将判断该msn是否是本机，如果不是则认为是黑客行为 拒绝登录

"""


def aes_encrypt(msn, key):
    """
    aes加密
    """
    from uuid import getnode
    iv = str(getnode())
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encryted_msn = cipher.encrypt(msn)
    return encryted_msn


def aes_decrypt(encrypted_msn, key):
    """
    aes解密
    :param message:
    :param key:
    :param iv:
    :return:
    """
    from uuid import getnode
    iv = str(getnode())
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msn = cipher.decrypt(encrypted_msn)
    return msn


def pbkdf2_sha256(password, salt, iterations=100000, dklen=32):
    """
    pbkdf2_sha256 加密是单向的 常用于密码的保存

    similar as hashlib.pbkdf2_hmac
    :return:
    """
    from Crypto.Hash import HMAC, SHA256
    from Crypto.Protocol.KDF import PBKDF2
    prf = lambda p, s: HMAC.new(p, s, SHA256).digest()
    key = PBKDF2(password, salt, dklen, iterations, prf)

    return key


def encrypt_message(message, key):
    """
    key is bytes
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    nonce = cipher.nonce

    ciphertext_info = '_'.join([
        binascii.hexlify(ciphertext).decode(),
        binascii.hexlify(tag).decode(),
        binascii.hexlify(nonce).decode()
    ])

    return ciphertext_info


def decrypt_message(ciphertext_info, key):
    """
    key is bytes
    :param ciphertext_info:
    :param key:
    :return:
    """
    ciphertext, tag, nonce = ciphertext_info.split('_')
    ciphertext = binascii.unhexlify(ciphertext)
    tag = binascii.unhexlify(tag)
    nonce = binascii.unhexlify(nonce)
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    message = cipher.decrypt_and_verify(ciphertext, tag)
    message = message.decode()
    return message


def get_wmic_uuid():
    """
    windows下 根据wmic命令 来获取机器唯一码 连接号已经去掉了
    :return:
    """
    cmd = 'wmic csproduct get uuid'

    output = subprocess.check_output(cmd).decode()
    uuid = output.split()[1]
    uuid = uuid.replace('-', '')
    return uuid
