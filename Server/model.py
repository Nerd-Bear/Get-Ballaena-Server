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

    @staticmethod
    def get_team_by_team_name(team_name: str) -> 'TeamModel':
        return TeamModel.objects(team_name=team_name).first()

    @staticmethod
    def get_all_teams() -> List['TeamModel']:
        return TeamModel.objects().all()


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

    @staticmethod
    def get_all_stamps() -> List['StampModel']:
        return StampModel.objects().all()

    @staticmethod
    def get_stamp_by_stamp_name(stamp_name: str):
        return StampModel.objects(stamp_name=stamp_name).first()


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

    @staticmethod
    def get_user_by_device_uuid(device_uuid: str) -> 'UserModel':
        return UserModel.objects(device_uuid=device_uuid).first()

    @staticmethod
    def get_user_by_name(name: str) -> 'UserModel':
        return UserModel.objects(name=name).first()

    @staticmethod
    def get_users_by_team(team: TeamModel) -> List['UserModel']:
        return UserModel.objects(team=team).all()

    @staticmethod
    def create(device_uuid: str, name: str):
        return UserModel(device_uuid=device_uuid, name=name).save()

    def capture_stamp(self, stamp: StampModel):
        self.stamps.append(stamp)
        return self.save()

    def is_captured_stamp(self, stamp: StampModel):
        return stamp in self.stamps

    def is_captured_all_stamps(self):
        return len(self.stamps) == len(StampModel.get_all_stamps())


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

    @staticmethod
    def create(coupon_name: str, user=UserModel):
        return CouponModel(coupon_name=coupon_name, user=user).save()
