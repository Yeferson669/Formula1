import base64

def b64encode(data):
    if data:
        return base64.b64encode(data).decode("utf-8")
    return ""
