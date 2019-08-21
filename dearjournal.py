#!/usr/bin/env python3
import os
from datetime import datetime
from pathlib import Path

ROOT_VAR = "DEARJOURNAL_ROOT"


def path_for(instant: datetime) -> Path:
    try:
        root = Path(os.environ[ROOT_VAR])
    except KeyError:
        raise RuntimeError("missing env var {!r}".format(ROOT_VAR))
    return (
        root
        / instant.strftime("%Y")
        / instant.strftime("%m")
        / "{}.txt".format(instant.strftime("%d"))
    )


if __name__ == "__main__":
    now = datetime.now()
    path = path_for(now)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

    with path.open("a") as f:
        f.write("\n::: {}\n\n".format(now.strftime("%H:%M:%S")))

    editor = os.getenv("EDITOR", "vi")
    opts = ["--", str(path)]
    if editor in {"vi", "vim", "nvim"}:
        opts = [editor, "+normal Go", *opts]

    os.execvp(editor, opts)
