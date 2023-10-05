import base64


def convert_to_base64(image):
    return base64.b64encode(image).decode('utf-8')
