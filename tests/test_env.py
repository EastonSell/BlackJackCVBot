import os
import importlib
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_num_decks_env():
    os.environ["NUM_DECKS"] = "6"
    import app.main as main
    importlib.reload(main)
    client = TestClient(main.app)
    assert main.card_counter.num_decks == 6
    os.environ.pop("NUM_DECKS", None)
    importlib.reload(main)
