import os
import re
from datetime import datetime
import pytz
from config import MEMORY_DIR

ET = pytz.timezone("America/New_York")


def read(filename):
    path = os.path.join(MEMORY_DIR, filename)
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(filename, content):
    path = os.path.join(MEMORY_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def append(filename, entry):
    path = os.path.join(MEMORY_DIR, filename)
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"\n{entry}\n")


def now_et():
    return datetime.now(ET).strftime("%Y-%m-%d %H:%M ET")


def today_et():
    return datetime.now(ET).strftime("%Y-%m-%d")


def get_flag(filename, key):
    content = read(filename)
    for line in content.splitlines():
        if line.strip().startswith(f"{key}:"):
            return line.split(":", 1)[1].strip()
    return None


def set_flag(filename, key, value):
    content = read(filename)
    pattern = rf"^({re.escape(key)}:\s*).*$"
    new_line = f"{key}: {value}"
    if re.search(pattern, content, flags=re.MULTILINE):
        content = re.sub(pattern, new_line, content, flags=re.MULTILINE)
    else:
        content += f"\n{new_line}"
    write(filename, content)
