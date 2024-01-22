import random


def pick_key():
    api_keys = [
        "ZrQEPSkKYWxleGFuZHJvc2xpYXBhdGVzQGdtYWlsLmNvbQ==",
        "ZrQEPSkKeXJpYWthZkBnbWFpbC5jb20=",
        "ZrQEPSkKYWxleDgyMDA5QHdpbmRvd3NsaXZlLmNvbQ==",
    ]
    return random.choice(api_keys)
