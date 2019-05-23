import os
from enum import Enum

STAFF_CODE = os.getenv('STAFF_CODE', '20190607')
ADMIN_CODE = os.getenv('ADMIN_CODE', 'nerd-bear')

TEAM_NAMES = (
    '밍크고래팀',
    '혹등고래팀',
    '대왕고래팀',
    '향유고래팀',
)
TEAM_COUNT = 3
MAX_TEAM_MEMBER_COUNT = 10


class TIME_CHECK(Enum):
    BEFORE_START = 0
    DURING_TIME = 1
    AFTER_END = 2
