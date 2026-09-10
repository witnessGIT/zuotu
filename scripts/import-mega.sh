#!/usr/bin/env bash
set -euo pipefail

# MEGA → Git 素材导入入口。修改此文件会触发 GitHub Actions 导入。
MEGA_URL="${1:-https://mega.nz/folder/boFk0TiD#iX6HknzaJ_VFFyxK56VCLQ}"
DEST="${2:-素材/郭文贵/mega}"

mkdir -p "$DEST"

if command -v mega-get >/dev/null 2>&1; then
  mega-get "$MEGA_URL" "$DEST"
elif command -v megadl >/dev/null 2>&1; then
  megadl "$MEGA_URL" --path "$DEST"
else
  echo "未检测到 MEGAcmd/megadl。请先安装 MEGAcmd，然后重新运行。" >&2
  exit 2
fi

echo "MEGA 素材已导入到: $DEST"
find "$DEST" -type f | sort
