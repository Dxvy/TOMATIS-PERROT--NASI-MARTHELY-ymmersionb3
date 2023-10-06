import base64
import hashlib


def convert_to_base64(image):
    return base64.b64encode(image).decode('utf-8')


def generate_salt():
    return hashlib.sha512().hexdigest()[:16]


def get_size(elem):
    return elem[3]


def get_price(elem):
    return elem[6]


def filter_by_price(lst, select_price):
    if select_price == "not-sorted":
        return lst
    elif select_price == "low-to-high":
        return lst.sort(key=get_price)
    else:
        return lst.sort(key=get_price, reverse=True)


def filter_by_type(lst, select_type):
    if select_type != "all":
        for elem in lst[:]:
            if elem[2] != select_type:
                lst.remove(elem)
    return lst


def filter_by_size(lst, select_size):
    if select_size != "all":
        for elem in lst[:]:
            if elem[3] != select_size:
                lst.remove(elem)
    return lst
