#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
design-partner GitHub 发布器（REST API 版）

为什么不用 git push：
    某些受管环境对 github.com（git 主机）做了出口拦截，只放通 api.github.com。
    此时 git push 必然失败，但 REST API 仍可用。本脚本用 Git Data API
    一次性把本地已跟踪文件打成单个 commit 推上去。

令牌来源（按优先级）：
    1. 环境变量 GITHUB_TOKEN
    2. 文件 ~/.workbuddy-ai/secrets/github_token（首行）
    3. --token 参数

令牌要求：fine-grained PAT，对该仓库授予 Contents: Read and write。

用法:
    python scripts/publish_github.py                 # 推送到默认仓库
    python scripts/publish_github.py --dry-run       # 只列将要推送的文件
    python scripts/publish_github.py --repo owner/name --message "feat: xxx"
"""
import json
import time
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REPO = "Soren-Blade/design-partner"
SECRET_DIR = Path.home() / ".workbuddy-ai" / "secrets"
# 兼容带扩展名/不带扩展名的写法
TOKEN_CANDIDATES = [
    SECRET_DIR / "github_token",
    SECRET_DIR / "github_token.txt",
    SECRET_DIR / "github_pat",
    SECRET_DIR / "github_pat.txt",
]
API = "https://api.github.com"


def die(msg):
    print(f"[失败] {msg}")
    sys.exit(1)


def get_token(argv):
    if "--token" in argv:
        return argv[argv.index("--token") + 1].strip()
    tok = os.environ.get("GITHUB_TOKEN", "").strip()
    if tok:
        return tok
    for cand in TOKEN_CANDIDATES:
        if cand.exists():
            lines = cand.read_text(encoding="utf-8").strip().splitlines()
            if lines and lines[0].strip():
                return lines[0].strip()
    die(
        "找不到令牌。请任选其一：\n"
        f"  1) 把 PAT 写入 {TOKEN_CANDIDATES[0]}（或同名 .txt，首行，仅自己可读）\n"
        "  2) 设置环境变量 GITHUB_TOKEN\n"
        "  3) 传 --token <PAT>\n"
        "令牌需为 fine-grained PAT，授予目标仓库 Contents: Read and write。"
    )


def call(method, path, token, payload=None, ok=(200, 201), retries=4):
    """带重试的 API 调用。

    本机到 api.github.com 的连接偶发被中途掐断（RemoteDisconnected），
    单次调用失败不代表接口不可用；因此对网络类错误与 5xx 做指数退避重试，
    并显式声明 Connection: close 避免复用被代理破坏的长连接。
    """
    url = path if path.startswith("http") else API + path
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "design-partner-publisher")
        req.add_header("Connection", "close")
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                body = r.read().decode("utf-8")
                return r.status, (json.loads(body) if body.strip() else {})
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            if e.code in ok:
                return e.code, {}
            # 4xx（除 429）是确定性错误，重试无意义
            if e.code < 500 and e.code != 429:
                raise RuntimeError(f"{method} {path} -> {e.code} {detail}")
            last = f"{e.code} {detail}"
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            last = f"网络错误: {getattr(e, 'reason', e)}"
        except Exception as e:  # http.client.RemoteDisconnected 等
            last = f"{type(e).__name__}: {e}"
        if attempt < retries - 1:
            wait = 2 * (attempt + 1)
            print(f"    重试 {attempt + 1}/{retries - 1}（{last[:60]}）… 等待 {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"{method} {path} -> 重试 {retries} 次仍失败: {last}")


def tracked_files():
    """用 git 取已跟踪文件，保证与本地提交一致。"""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "-z"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8")
        files = [f for f in out.split("\0") if f]
        if files:
            return files
    except Exception:
        pass
    # 无 git 时回退到目录遍历
    files = []
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and not any(
            part in {".git", "__pycache__", ".workbuddy-ai"} for part in p.parts
        ):
            files.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return files


def last_commit_message():
    try:
        return subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--pretty=%B"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8").strip()
    except Exception:
        return "chore: sync design-partner"


def main():
    argv = sys.argv[1:]
    dry = "--dry-run" in argv
    repo = DEFAULT_REPO
    if "--repo" in argv:
        repo = argv[argv.index("--repo") + 1]
    message = last_commit_message()
    if "--message" in argv:
        message = argv[argv.index("--message") + 1]

    files = tracked_files()
    print(f"=== 发布 {repo} ===")
    print(f"文件数: {len(files)}")

    if dry:
        for f in files:
            size = (ROOT / f).stat().st_size
            print(f"  {size:>7} B  {f}")
        print("(dry-run，未推送)")
        return

    token = get_token(argv)
    owner, name = repo.split("/", 1)

    # 1. 仓库信息与当前 head
    st, info = call("GET", f"/repos/{owner}/{name}", token)
    branch = info.get("default_branch") or "main"
    head_sha = None
    try:
        st, ref = call("GET", f"/repos/{owner}/{name}/git/ref/heads/{branch}", token)
        head_sha = ref.get("object", {}).get("sha")
    except RuntimeError as e:
        # 404 = 分支不存在；409 = 空仓库（Git Repository is empty）
        if not any(code in str(e) for code in ("404", "409")):
            raise
    print(f"分支: {branch} · 当前 head: {head_sha or '(空仓库)'}")

    # 1.5 空仓库引导：Git Data API 不能在没有提交的仓库里建 blob（409），
    #     必须先用 Contents API 写入第一个文件完成初始化。
    if not head_sha:
        boot = next((f for f in files if f == "README.md"), files[0] if files else None)
        if not boot:
            die("没有可推送的文件")
        import base64
        content_b64 = base64.b64encode(
            (ROOT / boot).read_text(encoding="utf-8").encode("utf-8")
        ).decode("ascii")
        call(
            "PUT", f"/repos/{owner}/{name}/contents/{boot}", token,
            {"message": f"chore: 初始化仓库（{boot}）", "content": content_b64},
        )
        print(f"  引导提交: {boot}")
        st, ref = call("GET", f"/repos/{owner}/{name}/git/ref/heads/{branch}", token)
        head_sha = ref.get("object", {}).get("sha")

    # 2. 逐个上传 blob
    tree = []
    for f in files:
        p = ROOT / f
        if not p.exists():
            print(f"  跳过（已删除）: {f}")
            continue
        content = p.read_text(encoding="utf-8")
        st, blob = call(
            "POST", f"/repos/{owner}/{name}/git/blobs", token,
            {"content": content, "encoding": "utf-8"},
        )
        tree.append({"path": f, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print(f"  ✓ {f}")

    # 3. 建 tree（不带 base_tree，即整树替换为本地状态）
    st, new_tree = call(
        "POST", f"/repos/{owner}/{name}/git/trees", token, {"tree": tree}
    )

    # 4. 建 commit
    payload = {"message": message, "tree": new_tree["sha"]}
    if head_sha:
        payload["parents"] = [head_sha]
    st, commit = call("POST", f"/repos/{owner}/{name}/git/commits", token, payload)

    # 5. 更新或创建 ref
    if head_sha:
        call(
            "PATCH", f"/repos/{owner}/{name}/git/refs/heads/{branch}", token,
            {"sha": commit["sha"], "force": False},
        )
    else:
        call(
            "POST", f"/repos/{owner}/{name}/git/refs", token,
            {"ref": f"refs/heads/{branch}", "sha": commit["sha"]},
        )

    print(f"\n[完成] commit {commit['sha'][:10]} → https://github.com/{repo}")


if __name__ == "__main__":
    main()
