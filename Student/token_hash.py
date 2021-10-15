import base64
import datetime
import random
from .redis_catch import set, get


def hash_encode(message):
    '''
    message:views传过来的用户id
    :param message:
    :return:
    '''
    # 获取当前时间并转换成标准格式字符串类型
    time = datetime.datetime.now()
    time_need = time.strftime('%Y-%m-%d %H:%M')
    # 加盐
    salt = random.randrange(1000000)
    # 加密
    token = base64.b64encode((message + '|' + time_need + '|' + str(salt)).encode('utf8'))
    # 存入缓存
    set(message, token)
    return token.decode()


def hash_decode(token):
    '''
    token:为前端提供的token，校对
    :param message:
    :return:
    '''
    # 解密
    if token:
        en_message = base64.b64decode(token.encode()).decode('utf8')
        list_message = en_message.split('|')
        key = list_message[0]
        # 当前时间转成字符串
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        # 当前时间转换成标准格式时间类型
        time_now = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M')
        salt = list_message[1]
        # 从缓存中拿出token
        token_catch = get(key)
        print(token_catch)
        # 解密token
        token_s = base64.b64decode(token_catch).decode('utf8')
        token_list = token_s.split('|')
        # token中的时间转换成标准时间类型
        token_time = datetime.datetime.strptime(token_list[1], '%Y-%m-%d %H:%M')
        # 判断token中的用户id，加盐值以及时间差是否符合
        if token_list[0] == key and str(token_list[1]) == str(salt) and (time_now - token_time).seconds <= 60 * 60:
            print('解密成功')
            return token_list[0]
        return False
    else:
        return False
