# name: 联通云盘活动
# cron: 0 0 2,8 * * *
import os
import platform
import subprocess
import sys
import stat
import urllib.request
import hashlib
import json

# ── 配置 ──────────────────────────────────────────────────────────────
GITHUB_RAW_BASE = "http://gh.301.ee/https://raw.githubusercontent.com/Aellyt/kele/main/yphd"
GITHUB_API_BASE = "https://api.github.com/repos/Aellyt/kele/contents/yphd"
TARGET          = "yphd_x86_64_py311"
DOWNLOAD_DIR    = "/ql/data/scripts/yphd"

# ── 判断是否 Alpine ────────────────────────────────────────────────────
if not os.path.exists("/etc/alpine-release"):
    print("❌ 非 Alpine 系统，停止运行")
    sys.exit(0)

print("✅ Alpine 系统检测通过")

# ── 判断架构 ──────────────────────────────────────────────────────────
arch = platform.machine().lower()
print(f"当前架构: {arch}")

if "x86_64" not in arch and "amd64" not in arch:
    print(f"❌ 非 x86_64 架构（{arch}），停止运行")
    sys.exit(0)

print("✅ 架构检测通过：x86_64")

# ── 工具函数 ──────────────────────────────────────────────────────────
def git_blob_sha1(path: str) -> str:
    size = os.path.getsize(path)
    h = hashlib.sha1()
    h.update(f"blob {size}\0".encode())
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def get_remote_sha() -> str | None:
    url = f"{GITHUB_API_BASE}/{TARGET}"
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.github+json",
        })
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data.get("sha")
    except Exception as e:
        print(f"⚠️ 获取远程 sha 失败: {e}")
        return None

def download():
    url = f"{GITHUB_RAW_BASE}/{TARGET}"
    print(f"正在下载: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(save_path, "wb") as f:
        f.write(resp.read())
    print(f"✅ 下载成功: {save_path}")

# ── 主逻辑 ────────────────────────────────────────────────────────────
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
save_path = os.path.join(DOWNLOAD_DIR, TARGET)

if os.path.exists(save_path):
    print("📁 本地文件已存在，校验中...")
    try:
        with open(save_path, "rb") as f:
            f.read(1)
    except Exception:
        print("⚠️ 文件不可读，重新下载")
        os.remove(save_path)
        try:
            download()
        except Exception as e:
            print(f"❌ 下载失败: {e}")
            sys.exit(1)
    else:
        remote_sha = get_remote_sha()
        if remote_sha is None:
            print("⚠️ 无法获取远程版本，直接使用本地文件")
        else:
            local_sha = git_blob_sha1(save_path)
            print(f"本地 sha: {local_sha}")
            print(f"远程 sha: {remote_sha}")
            if local_sha == remote_sha:
                print("✅ 文件一致，无需下载")
            else:
                print("🔄 文件有更新，重新下载")
                try:
                    download()
                except Exception as e:
                    print(f"❌ 下载失败: {e}")
                    sys.exit(1)
else:
    print("📥 本地文件不存在，开始下载")
    try:
        download()
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        sys.exit(1)

# ── 授权并执行 ────────────────────────────────────────────────────────
os.chmod(save_path, os.stat(save_path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
print("✅ 已授予执行权限")

print(f"正在运行: {save_path}")
result = subprocess.run([save_path], capture_output=False)
sys.exit(result.returncode)
