import os
import logging
from datetime import datetime
import pytz
import git
from config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH, ROOT_DIR

log = logging.getLogger(__name__)
ET = pytz.timezone("America/New_York")


def _repo():
    return git.Repo(ROOT_DIR)


def pull():
    try:
        repo = _repo()
        origin = repo.remotes.origin
        origin.pull(GITHUB_BRANCH)
        log.info("git pull complete")
    except Exception as e:
        log.warning(f"git pull failed (may be first run): {e}")


def push(message):
    try:
        repo = _repo()
        repo.index.add(["memory/"])
        if not repo.index.diff("HEAD") and not repo.untracked_files:
            log.info("Nothing to commit")
            return
        now = datetime.now(ET).strftime("%Y-%m-%d %H:%M ET")
        full_msg = f"{message} | {now}"
        repo.index.commit(full_msg)
        origin = repo.remotes.origin
        remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
        origin.set_url(remote_url)
        origin.push(GITHUB_BRANCH)
        log.info(f"Pushed: {full_msg}")
    except Exception as e:
        log.error(f"git push failed: {e}")


def setup_remote(remote_url=None):
    repo = _repo()
    url = remote_url or f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
    if "origin" not in [r.name for r in repo.remotes]:
        repo.create_remote("origin", url)
    else:
        repo.remotes.origin.set_url(url)
    log.info(f"Remote set to {GITHUB_REPO}")
