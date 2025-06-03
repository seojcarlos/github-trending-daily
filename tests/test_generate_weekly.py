import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import datetime as dt
from datetime import datetime, timedelta, timezone

import generate_weekly as gw

class MockDateTime:
    UTC = timezone.utc
    @staticmethod
    def now(tz):
        return datetime.now(tz)


def create_history_files(base_dir, days_to_create):
    history_dir = base_dir / "trending_history"
    history_dir.mkdir()
    today = datetime.now(timezone.utc)
    created = []
    for i in days_to_create:
        day = today - timedelta(days=i)
        fname = history_dir / f"{day.strftime('%Y-%m-%d')}.md"
        fname.write_text("test")
        created.append(str(fname))
    return created


def test_get_last_n_days_files_only_existing(tmp_path, monkeypatch):
    created = create_history_files(tmp_path, [0, 2, 3])
    monkeypatch.setattr(gw, "HIST_DIR", str(tmp_path / "trending_history"))
    monkeypatch.setattr(gw, "datetime", MockDateTime)
    files = gw.get_last_n_days_files(5)
    expected = created
    assert files == expected
