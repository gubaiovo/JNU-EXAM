#!/bin/bash
set -e

REPO_DIR="/app/repo"
INTERVAL=${AUTO_UPDATE_INTERVAL:-0}
MAX_RETRIES=3 
RETRY_DELAY=5 

echo "JNU-EXAM Docker 镜像站启动..."

update_content() {
    generate_json() {
        echo "生成目录结构 JSON..."
        python3 /app/generate_json.py || echo "JSON 生成失败"
    }

    echo "[$(date +%H:%M:%S)] 开始检查更新..."

    if [ -d "$REPO_DIR/.git" ]; then
        cd $REPO_DIR
        
        set +e
        git checkout . >/dev/null 2>&1
        set -e

        count=0
        success=0
        while [ $count -lt $MAX_RETRIES ]; do
            set +e 
            GIT_OUTPUT=$(git pull 2>&1)
            EXIT_CODE=$?
            set -e

            if [ $EXIT_CODE -eq 0 ]; then
                success=1
                break
            else
                count=$((count + 1))
                echo "⚠️ Git pull 连接失败 (尝试 $count/$MAX_RETRIES):"
                echo "$GIT_OUTPUT"
                
                if [ $count -lt $MAX_RETRIES ]; then
                    echo "等待 ${RETRY_DELAY} 秒后重试..."
                    sleep $RETRY_DELAY
                fi
            fi
        done
        if [ $success -eq 0 ]; then
            echo "❌ 多次重试 Git 更新均失败。"
            echo "⏭️ 跳过本次更新，将在 ${INTERVAL} 秒后进行下一次尝试。"
            return 
        fi

        echo "$GIT_OUTPUT"
        
        generate_json

    else
        echo "非 Git 仓库模式，仅重新生成 JSON。"
        generate_json
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