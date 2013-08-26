import peewee
from pyramid_peewee import get_management as factory

BaseModelManagement = factory()
BaseModel = BaseModelManagement.get_base()            

class User(BaseModel):
    username = peewee.CharField()
    password = peewee.CharField()

    def __repr__(self):
        return u"<User name: %s>" % self.username

class Message(BaseModel):
    user = peewee.ForeignKeyField(User)
    content = peewee.TextField()
    pub_date = peewee.DateTimeField()

    def __repr__(self):
        return u"<Message user: %s,  pub_date: %s>" % (self.user.username, self.pub_date)

def get_management():
    return BaseModelManagement
