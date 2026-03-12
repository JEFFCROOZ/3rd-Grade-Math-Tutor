"""
File-based persistence layer for tracking practice progress.
No Streamlit imports. Uses atomic writes to prevent corruption.
"""

import json
import os
from datetime import datetime, date

# Anchor path to project root (parent of utils/) regardless of launch CWD
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_PROJECT_ROOT, "data")
if not os.access(_PROJECT_ROOT, os.W_OK):
    # Streamlit Cloud mounts source as read-only; fall back to /tmp
    _DATA_DIR = "/tmp/math-tutor-data"
PROGRESS_FILE = os.path.join(_DATA_DIR, "progress.json")

# Postgres backend — used when DATABASE_URL is set in the environment
_DATABASE_URL = os.environ.get("DATABASE_URL")


def _pg_connect():
    import psycopg2
    return psycopg2.connect(_DATABASE_URL)


def _pg_ensure_table():
    with _pg_connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY DEFAULT 1,
                    data JSONB NOT NULL,
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)


_DEFAULT_TOPIC = {"attempted": 0, "correct": 0, "stars": 0, "last_practiced": None}

_DEFAULT_SCHEMA = {
    "meta": {
        "created": None,
        "last_updated": None,
        "schema_version": "1.0",
        "focus_topic": None,
    },
    "totals": {
        "stars": 0,
        "problems_attempted": 0,
        "problems_correct": 0,
    },
    "topics": {
        "3OA": dict(_DEFAULT_TOPIC),
        "3NBT": dict(_DEFAULT_TOPIC),
        "3NF": dict(_DEFAULT_TOPIC),
        "3MD": dict(_DEFAULT_TOPIC),
        "3G": dict(_DEFAULT_TOPIC),
    },
    "sessions": [],
    "wrong_attempts": [],
}

_MAX_SESSIONS = 30
_MAX_WRONG_ATTEMPTS = 100


def load_progress() -> dict:
    if _DATABASE_URL:
        try:
            _pg_ensure_table()
            with _pg_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT data FROM progress WHERE id = 1")
                    row = cur.fetchone()
                    if row:
                        return row[0]  # psycopg2 returns JSONB as a Python dict
        except Exception:
            pass  # fall through to file backend
    if not os.path.exists(PROGRESS_FILE):
        data = json.loads(json.dumps(_DEFAULT_SCHEMA))
        data["meta"]["created"] = datetime.now().isoformat()
        return data
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        data = json.loads(json.dumps(_DEFAULT_SCHEMA))
        data["meta"]["created"] = datetime.now().isoformat()
        return data


def save_progress(data: dict) -> None:
    data["meta"]["last_updated"] = datetime.now().isoformat()
    if _DATABASE_URL:
        try:
            _pg_ensure_table()
            with _pg_connect() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO progress (id, data, updated_at)
                        VALUES (1, %s, NOW())
                        ON CONFLICT (id) DO UPDATE
                            SET data = EXCLUDED.data, updated_at = NOW()
                    """, (json.dumps(data),))
            return
        except Exception:
            pass  # fall through to file backend
    os.makedirs(_DATA_DIR, exist_ok=True)
    tmp_path = PROGRESS_FILE + ".tmp"
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    os.replace(tmp_path, PROGRESS_FILE)


def record_attempt(
    topic_key: str,
    subtopic: str,
    problem_dict: dict,
    user_answer: str,
    is_correct: bool,
    hint_used: bool,
) -> None:
    data = load_progress()
    now = datetime.now().isoformat()
    today = date.today().isoformat()

    # Update totals
    data["totals"]["problems_attempted"] += 1
    if is_correct:
        data["totals"]["problems_correct"] += 1
        data["totals"]["stars"] += 1

    # Update topic stats
    if topic_key not in data["topics"]:
        data["topics"][topic_key] = dict(_DEFAULT_TOPIC)
    data["topics"][topic_key]["attempted"] += 1
    if is_correct:
        data["topics"][topic_key]["correct"] += 1
        data["topics"][topic_key]["stars"] += 1
    data["topics"][topic_key]["last_practiced"] = today

    # Record wrong attempts
    if not is_correct:
        entry = {
            "timestamp": now,
            "topic": topic_key,
            "subtopic": subtopic,
            "problem_text": problem_dict.get("problem_text", ""),
            "correct_answer": problem_dict.get("answer", ""),
            "user_answer": user_answer,
            "hint_used": hint_used,
            "explanation_child": problem_dict.get("explanation_child", ""),
            "explanation_parent": problem_dict.get("explanation_parent", ""),
        }
        data["wrong_attempts"].append(entry)
        # Cap at max
        if len(data["wrong_attempts"]) > _MAX_WRONG_ATTEMPTS:
            data["wrong_attempts"] = data["wrong_attempts"][-_MAX_WRONG_ATTEMPTS:]

    save_progress(data)


def open_session(topic_key: str) -> str:
    """Record session start, return ISO timestamp as session ID."""
    return datetime.now().isoformat()


def close_session(
    session_start: str,
    topic_key: str,
    problems_attempted: int,
    problems_correct: int,
    stars_earned: int,
) -> None:
    data = load_progress()
    start_dt = datetime.fromisoformat(session_start)
    end_dt = datetime.now()
    session = {
        "date": start_dt.date().isoformat(),
        "timestamp": session_start,
        "topic": topic_key,
        "problems_attempted": problems_attempted,
        "problems_correct": problems_correct,
        "stars_earned": stars_earned,
        "duration_seconds": int((end_dt - start_dt).total_seconds()),
    }
    data["sessions"].append(session)
    if len(data["sessions"]) > _MAX_SESSIONS:
        data["sessions"] = data["sessions"][-_MAX_SESSIONS:]
    save_progress(data)


def get_all_stats() -> dict:
    data = load_progress()
    return {
        "totals": data["totals"],
        "topics": data["topics"],
    }


def get_topic_stats(topic_key: str) -> dict:
    data = load_progress()
    return data["topics"].get(topic_key, dict(_DEFAULT_TOPIC))


def get_recent_sessions(n: int = 5) -> list:
    data = load_progress()
    return list(reversed(data["sessions"]))[:n]


def get_wrong_attempts(topic_key: str = None) -> list:
    data = load_progress()
    attempts = data["wrong_attempts"]
    if topic_key:
        attempts = [a for a in attempts if a["topic"] == topic_key]
    return list(reversed(attempts))


def get_star_count() -> int:
    data = load_progress()
    return data["totals"]["stars"]


def set_focus_topic(topic_key: str) -> None:
    data = load_progress()
    data["meta"]["focus_topic"] = topic_key
    save_progress(data)


def get_focus_topic():
    data = load_progress()
    return data["meta"].get("focus_topic")
