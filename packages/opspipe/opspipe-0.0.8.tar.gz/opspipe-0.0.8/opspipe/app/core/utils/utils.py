"""
助手工具
"""
import hashlib
import qrcode
import base64
from io import BytesIO
import uuid
import time


# 密码加密
def en_password(psw: str):
    p = hashlib.md5(psw.encode(encoding='UTF-8')).hexdigest()
    return p


# 密码校验你
def check_password(password: str, old: str):
    np = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
    if np == old:
        return True
    else:
        return False


# 字符串转二维码图片二进制
def str_qrcode(txt: str):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=4,
    )

    qr.add_data(txt)
    qr.make(fit=True)
    img = qr.make_image()
    return img


# 图片转base64
def img_base64(img: bytes):
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    # base64头
    header = "data:image/png;base64,"
    base64_data = header + str(base64_data.decode('utf-8'))
    return base64_data


# 唯一随机字符串
def only_str():
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)


# 毫秒时间戳
def get_times():
    return int(round(time.time() * 1000))


# 生成token
def create_token(uid: int):
    t = str(uuid.uuid1()) + str(uid)
    return hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()
