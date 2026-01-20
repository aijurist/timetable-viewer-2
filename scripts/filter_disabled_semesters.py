"""Filter out disabled semesters from schedule JSON files.
Creates a backup (.bak) and rewrites the original files without entries
matching semesters in DISABLED_SEMESTERS.
"""
import json
import shutil
from pathlib import Path

DISABLED_SEMESTERS = {4}
FILES = [Path("data/lab_schedule.json"), Path("data/theory_schedule.json")]


def get_semester_num(item):
    sem = item.get("semester")
    if isinstance(sem, int):
        return sem
    if isinstance(sem, str):
        import re

        m = re.search(r"(\d+)", sem)
        if m:
            return int(m.group(1))
    grp = item.get("group_name") or ""
    import re

    m = re.search(r"_S(\d+)_|_S(\d+)$|S(\d+)", grp)
    if m:
        for g in m.groups():
            if g:
                return int(g)
    return None


def process_file(path: Path):
    if not path.exists():
        print(f"Skipping missing file: {path}")
        return
    bak = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, bak)
    print(f"Backup created: {bak}")

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        print(f"Unexpected format in {path}: expected list at top level")
        return

    original_count = len(data)
    filtered = []
    removed = 0
    for item in data:
        sem = get_semester_num(item)
        if sem is not None and sem in DISABLED_SEMESTERS:
            removed += 1
            continue
        filtered.append(item)

    with path.open("w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)

    print(f"Processed {path}: original={original_count}, removed={removed}, remaining={len(filtered)}")


if __name__ == "__main__":
    for p in FILES:
        process_file(p)
    print("Done.")
