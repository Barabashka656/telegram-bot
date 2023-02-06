from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    DateTimeField,
    ForeignKeyField
)
import datetime
from data.config import DATABASE_DIR


db = SqliteDatabase(DATABASE_DIR)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(unique=True)
    first_name = CharField(max_length=64)
    username = CharField(null=True, max_length=32)
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'Users'
        order_by = 'created_at'


class YoutubeDlInfo(BaseModel):
    user_id = ForeignKeyField(model=User, field='user_id')
    file_id = CharField()
    yt_url = CharField()
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = 'YoutubeDlInfo'
        order_by = 'user_id'


class EpicFreeGame(BaseModel):
    title = CharField()
    description = CharField()
    product_slug = CharField()
    key_image_url = CharField()
    start_date = DateTimeField(null=True)
    end_date = DateTimeField(null=True)
    original_price = CharField()

    class Meta:
        db_table = 'EpicFreeGame'
        order_by = 'start_date'


class Utility(BaseModel):
    next_notification = DateTimeField(null=True)

    class Meta:
        db_table = 'Utility'


class EpicMail(BaseModel):
    user_id = ForeignKeyField(model=User, field='user_id')

    class Meta:
        db_table = 'EpicMail'
        order_by = 'user_id'


class ShortcutTable(BaseModel):
    user_id = ForeignKeyField(model=User, field='user_id')
    shortcut_source = CharField(max_length=11)

    class Meta:
        db_table = 'ShortcutTable'
        order_by = 'user_id'


def create_database():
    with db:
        models = [User, YoutubeDlInfo,
                  EpicFreeGame, EpicMail,
                  Utility, ShortcutTable
                  ]

        db.create_tables(models)
        # db.create_tables([EpicFreeGame])
