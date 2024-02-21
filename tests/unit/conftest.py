import pytest

from tests.mocks.dialogue_repo import DialogueRepoMock


@pytest.fixture
def dialogue_repo():
    return DialogueRepoMock()
