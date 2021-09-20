import pytest   # python -m pytest -v tests
from library import create_app
from library.adapters import memory_repository
from library.adapters.memory_repository import MemoryRepository
from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app()

    return my_app.test_client()
