from models import get_management
from models import User
from hashlib import md5

management = get_management()
management.setup("sqlite", "peeweee2.db")
management.populate()

def get_or_create_user(name, password):
    try:
        user = User.get(username=name)
    except User.DoesNotExist:
        user = User.create(
            username=name, 
            password=md5(password).hexdigest()
            )
    return user

print get_or_create_user("foo", "bar")
print get_or_create_user("boo", "bar")
print list(User.select().where(password=md5("bar").hexdigest()))
print User.select().where(password=md5("bar").hexdigest()).count()

# <User name: foo>
# <User name: boo>
# [<User name: foo>, <User name: boo>]
# 2

