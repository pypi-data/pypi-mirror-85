from .models import *
from .update import update_database


def get(*args, **kwargs):
    return Method.get(*args, **kwargs)

def search(*args, **kwargs):
    return Method.search(*args, **kwargs)

query = session.query(Method)
