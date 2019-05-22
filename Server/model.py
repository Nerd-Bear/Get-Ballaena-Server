from bson import ObjectId
from datetime import datetime
import json
from typing import List
from uuid import uuid4

from mongoengine import *

from const import TEAM_NAMES, TEAM_COUNT, MAX_TEAM_MEMBER_COUNT


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

    @staticmethod
    def create(team_name: str):
        TeamModel(team_name=team_name).save()

    @staticmethod
    def initialize():
        TeamModel.drop_collection()
        for team_name in TEAM_NAMES[TEAM_COUNT]:
            TeamModel.create(team_name=team_name)


class BoothModel(Document):
    meta = {
        "collection": "booth",
    }

    booth_name: str = StringField(
        primary_key=True,
        required=True,
    )

    own_team: TeamModel = ReferenceField(
        document_type=TeamModel,
    )

    next_capture_time: datetime = DateTimeField(
        default=datetime(2001, 4, 20),
    )

    x: int = IntField(
        required=True,
    )

    y: int = IntField(
        required=True,
    )

    @staticmethod
    def get_all_booths() -> List['BoothModel']:
        return BoothModel.objects().all()

    @staticmethod
    def create(booth_name: str, x: int, y: int):
        return BoothModel(booth_name=booth_name, x=x, y=y).save()

    @staticmethod
    def load_data():
        with open('data/booth.json') as f:
            booth_data = json.load(f)
        return booth_data

    @staticmethod
    def initialize():
        BoothModel.drop_collection()
        booth_data = BoothModel.load_data()

        for booth in booth_data:
            BoothModel.create(**booth)


class StampModel(Document):
    meta = {
        "collection": "stamp"
    }

    stamp_name: str = StringField(
        primary_key=True,
        required=True,
    )

    x: int = IntField(
        required=True,
    )

    y: int = IntField(
        required=True,
    )

    @staticmethod
    def get_all_stamps() -> List['StampModel']:
        return StampModel.objects().all()

    @staticmethod
    def get_stamp_by_stamp_name(stamp_name: str):
        return StampModel.objects(stamp_name=stamp_name).first()

    @staticmethod
    def create(stamp_name: str, x: int, y: int):
        return StampModel(stamp_name=stamp_name, x=x, y=y).save()

    @staticmethod
    def load_data():
        with open('data/stamp.json') as f:
            stamp_data = json.load(f)
        return stamp_data

    @staticmethod
    def initialize():
        StampModel.drop_collection()
        stamp_data = StampModel.load_data()

        for stamp in stamp_data:
            StampModel.create(**stamp)


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

    @staticmethod
    def create(content: str, answer: str, choices: List[str]):
        return ProblemModel(content=content, answer=answer, choices=choices).save()

    @staticmethod
    def load_data():
        with open('data/problem.json') as f:
            problem_data = json.load(f)
        return problem_data

    @staticmethod
    def initialize():
        ProblemModel.drop_collection()
        problem_data = ProblemModel.load_data()

        for problem in problem_data:
            ProblemModel.create(**problem)


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
    def get_all_users() -> QuerySet:
        return UserModel.objects().all()

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

    @staticmethod
    def initialize():
        users = UserModel.get_all_users()
        users.update(unset__team=1)

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

    @staticmethod
    def get_coupons_by_user(user: UserModel) -> List['CouponModel']:
        return CouponModel.objects(uset=user).all()

    @staticmethod
    def get_coupon_by_coupon_id_and_user(coupon_id: ObjectId, user: UserModel) -> 'CouponModel':
        return CouponModel.objects(coupon_id=coupon_id, user=user).first()

    @staticmethod
    def initialize():
        pass


def create_join_code():
    while True:
        t = str(uuid4())[:4]
        if not JoinCodeModel.get_join_code_by_code(t):
            return t


class JoinCodeModel(Document):
    meta = {
        'collection': 'join_code'
    }

    code = StringField(
        primary_key=True,
        default=create_join_code,
    )

    team = ReferenceField(
        TeamModel,
        required=True,
    )

    @staticmethod
    def get_join_code_by_code(code: str) -> 'JoinCodeModel':
        return JoinCodeModel.objects(code=code).first()

    @staticmethod
    def create(team: TeamModel) -> 'JoinCodeModel':
        return JoinCodeModel(team=team).save()

    @staticmethod
    def initialize():
        JoinCodeModel.drop_collection()
        for team in TeamModel.get_all_teams():
            for i in range(MAX_TEAM_MEMBER_COUNT):
                JoinCodeModel.create(team=team)
