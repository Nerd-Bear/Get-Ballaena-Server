from typing import List
from datetime import datetime

from mongoengine import *


class TeamModel(Document):

    meta = {
        'collection': 'team'
    }

    team_name: str = StringField(
        primary_key=True
    )


class BoothModel(Document):

    meta = {
        "collection": "booth"
    }

    booth_name: str = StringField(
        primary_key=True,
        required=True
    )

    own_team: TeamModel = ReferenceField(
        document_type=TeamModel
    )

    next_capture_time: datetime = DateTimeField(
        default=datetime(2001, 4, 20)
    )

    latitude: float = FloatField()

    longitude: float = FloatField()


class StampModel(Document):

    meta = {
        "collection": "stamp"
    }

    stamp_name: str = StringField(
        primary_key=True,
        required=True
    )

    x: int = IntField()

    y: int = IntField()


class ProblemModel(Document):

    meta = {
        'collection': 'problem'
    }

    content: str = StringField(
        required=True
    )

    answer: str = StringField(
        required=True
    )

    choices: List[str] = ListField(
        StringField(
            required=True
        )
    )


class UserModel(Document):

    meta = {
        'collection': 'user'
    }

    name: str = StringField(
        required=True
    )

    device_uuid: str = StringField(
        required=True
    )

    team: TeamModel = ReferenceField(
        document_type=TeamModel
    )

    stamps: List[StampModel] = ListField(
        ReferenceField(
            document_type=StampModel,
            reverse_delete_rule=CASCADE,
        ),
        default=[],
    )


class CouponModel(Document):

    meta = {
        'collection': 'coupon'
    }

    coupon_name: str = StringField(
        required=True
    )
    user: UserModel = ReferenceField(
        document_type=UserModel,
        reverse_delete_rule=CASCADE,
    )
