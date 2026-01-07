#!/bin/bash
set -e

REPO_DIR="/app/repo"
INTERVAL=${AUTO_UPDATE_INTERVAL:-0}

echo "JNU-EXAM Docker 镜像站启动..."

update_content() {
    echo "目录结构生成..."
    python3 /app/generate_json.py || echo "JSON 生成失败"
    echo "[$(date +%H:%M:%S)] 开始检查更新..."
    if [ -d "$REPO_DIR/.git" ]; then
        cd $REPO_DIR
        GIT_OUTPUT=$(git pull 2>&1)
        echo "$GIT_OUTPUT"
        
        if [[ "$GIT_OUTPUT" == *"Already up to date"* ]]; then
            echo "仓库已是最新，跳过 JSON 生成。"
            return
        fi
    else
        echo "非 Git 仓库模式，仅重新生成 JSON。"
    fi
}

run_scheduler() {
    echo "自动更新任务已启动，间隔: ${INTERVAL}秒"
    while true; do
        sleep "$INTERVAL"
        update_content
    done
}

if [ -z "$(ls -A $REPO_DIR)" ]; then
   echo "错误: /app/repo 为空！"
   echo "   Docker 未能正确挂载项目根目录。"
   echo "   请检查 docker-compose.yml 中 volumes 是否包含 '../:/app/repo'。"
   exit 1
fi

update_content

if [ "$INTERVAL" -gt 0 ]; then
    run_scheduler & 
else
    echo "ℹ️  自动更新已禁用 (AUTO_UPDATE_INTERVAL=0)"
fi

echo "启动 Web 服务器..."
nginx -g "daemon off;"