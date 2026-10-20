import os
import base64
import logging
from datetime import datetime
import pytz
import git
from config import GITHUB_TOKEN, GITHUB_REPO, GITHUB_BRANCH, ROOT_DIR

log = logging.getLogger(__name__)
ET = pytz.timezone("America/New_York")


def _repo():
    return git.Repo(ROOT_DIR)


def _git_env():
    # The token goes to git as an auth header via environment variables, so it is
    # never saved in .git/config or shown in a command line or error message.
    # Without a token, git uses the saved Git Credential Manager login instead.
    # Runs are unattended: fail fast rather than open a sign-in prompt and hang.
    env = {"GIT_TERMINAL_PROMPT": "0", "GCM_INTERACTIVE": "never"}
    if GITHUB_TOKEN:
        basic = base64.b64encode(f"x-access-token:{GITHUB_TOKEN}".encode()).decode()
        env.update({
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "http.https://github.com/.extraheader",
            "GIT_CONFIG_VALUE_0": f"AUTHORIZATION: basic {basic}",
        })
    return env


def pull():
    try:
        repo = _repo()
        origin = repo.remotes.origin
        with repo.git.custom_environment(**_git_env()):
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
        with repo.git.custom_environment(**_git_env()):
            origin.push(GITHUB_BRANCH)
        log.info(f"Pushed: {full_msg}")
    except Exception as e:
        log.error(f"git push failed: {e}")


def setup_remote(remote_url=None):
    repo = _repo()
    url = remote_url or f"https://github.com/{GITHUB_REPO}.git"
    if "origin" not in [r.name for r in repo.remotes]:
        repo.create_remote("origin", url)
    else:
        repo.remotes.origin.set_url(url)
    log.info(f"Remote set to {GITHUB_REPO}")
