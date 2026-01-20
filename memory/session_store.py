import json
from pathlib import Path

class SessionStore:
    def __init__(self, base_dir="sessions"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def load(self, investigation_id):
        path = self.base_dir / f"{investigation_id}.json"
        if path.exists():
            return json.loads(path.read_text())
        return None

    def save(self, investigation_id, state):
        path = self.base_dir / f"{investigation_id}.json"
        path.write_text(json.dumps(state, indent=2))