import pytest
from dotenv import load_dotenv

from utils.assertions import AssertionHelper

load_dotenv()


@pytest.fixture
def soft():
    assertions = AssertionHelper()
    yield assertions
    assertions.assert_all()
