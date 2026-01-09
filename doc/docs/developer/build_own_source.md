# 镜像站部署

**注意，PC端下载器使用镜像站请务必将下载器更新至 2.1.1 版本及以上**

如果你拥有服务器资源，欢迎搭建 JNU-EXAM 的镜像站，帮助更多同学获取资料。

本文档提供两种部署方式：

1. **Docker 部署**：开箱即用，自动同步 GitHub 资料
2. **手动部署**：适合有特殊定制需求或无法使用 Docker / 无法访问 Github 的环境

## 方式一：Docker 部署

我们提供了封装好的 Docker 镜像，内置了 Nginx 服务器和自动更新脚本。你无需配置 Python 环境或手动处理文件索引。

### 1. 基础准备

- 一台安装了 [Docker](https://docs.docker.com/get-docker/) 和 [Docker Compose](https://docs.docker.com/compose/install/) 的服务器
- 足够的磁盘空间（建议预留 10GB 以上，用于存放资料。本稿完成时资料文件总大小为 3G）

### 2. 获取配置文件

服务器克隆本项目仓库，并进入部署目录：

```shell
git clone https://github.com/gubaiovo/JNU-EXAM.git
cd JNU-EXAM/deployment
```

### 3. 配置下载源

默认情况下，镜像站使用官方的 Github 和 Cloudflare R2。如果你希望用户通过你的服务器下载文件（即把你的服务器作为直链源），请修改 `sources.json`。

在 `deployment` 目录下创建或修改 `sources.json`：

```
[
  {
    "name": "本站极速镜像",
    "base": "http://你的服务器IP或域名/data",
    "json_url": "http://你的服务器IP或域名/directory_structure.json",
    "type": "tree",
    "key": "mirror_url"
  },
  {
    "name": "官方 Github (备用)",
    "base": "[https://raw.githubusercontent.com/gubaiovo/JNU-EXAM/main/data](https://raw.githubusercontent.com/gubaiovo/JNU-EXAM/main/data)",
    "json_url": "[https://github.com/gubaiovo/JNU-EXAM/raw/main/directory_structure.json](https://github.com/gubaiovo/JNU-EXAM/raw/main/directory_structure.json)",
    "type": "tree"
  }
]
```

> **注意**：`base` 是文件下载的基础路径，`json_url` 是文件索引的访问路径。Docker 启动后会将资料映射到 Web 根目录，因此路径通常是 `/data` 和 `/directory_structure.json`。

### 4. 启动服务

在 `deployment` 目录下执行：

```
docker compose up -d
```

启动后，访问 `http://你的IP:8080/directory_structure.json` 看到索引文件内容，即为搭建成功

### 5. 自动更新设置

默认情况下，容器每 30 秒自动检查并拉取 GitHub 的最新资料。

如需修改频率，请编辑 `docker-compose.yml`：

```
environment:
  - AUTO_UPDATE_INTERVAL=3600  # 设置为 0 可关闭自动更新
```

## 方式二：手动部署

如果你想完全控制文件存储方式（如使用对象存储、本地 NAS 等），可以选择手动部署。

### 1. 获取资料

首先将资料库克隆到本地：

```shell
git clone https://github.com/gubaiovo/JNU-EXAM.git
```

### 2. 搭建服务

你需要一个 HTTP 服务来对外提供文件访问。

- **简单测试**：使用 Python 快速启动 `python -m http.server 8000`。
- **生产环境**：推荐使用 Nginx、Apache 或 对象存储服务，如[RustFS](https://rustfs.com.cn/)。

### 3. 生成索引文件

为了让下载器能正确显示文件列表，你需要生成 `directory_structure.json` 和 `source_list.json`。

我们提供了 Python 脚本来完成此工作：

1. 安装依赖：

   确保安装了 Python 3。

2. 配置脚本：

   修改 deployment/generate_json.py（或参考该逻辑编写自己的脚本），定义你的存储源 SOURCES：

   ```json
   SOURCES = [
       {
           "name": "我的本地源",
           "key": "local_url",
           "base": "http://你的域名/data",  # 文件下载前缀
           "type": "tree",                 # tree: 保持目录结构; flat: 扁平化(如蓝奏云)
           "enabled": True
       }
   ]
   ```

3. **运行生成**：

   ```shell
   python3 deployment/generate_json.py
   ```

   生成的 json 文件将位于项目根目录

## 配置文件详解 (sources.json)

无论是 Docker 还是手动部署，核心都在于定义**下载源**。以下是字段说明：

| **字段**   | **说明**                              | **示例**                                    |
| ---------- | ------------------------------------- | ------------------------------------------- |
| `name`     | 在前端显示的下载按钮名称              | `"校内镜像"`                                |
| `base`     | 文件下载的基础 URL 前缀               | `"http://1.2.3.4/data"`                     |
| `json_url` | **关键**：该源对应的索引文件地址      | `"http://1.2.3.4/directory_structure.json"` |
| `type`     | 目录结构类型。`tree` (默认) 或 `flat` | `"tree"`                                    |
| `key`      | 唯一标识符，建议使用英文              | `"school_mirror"`                           |

**工作原理：**

1. 用户访问你的镜像站
2. 网页读取 `source_list.json`，获取所有可用源的列表
3. 用户选择一个源，网页根据该源的 `json_url` 读取文件树
4. 点击下载时，网页将 `base` + `文件相对路径` 拼接成最终下载链接
