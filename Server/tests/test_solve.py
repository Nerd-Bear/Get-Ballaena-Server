from unittest import TestCase
from unittest.mock import MagicMock, patch

from app import create_app
from tests.request import check_status_code
