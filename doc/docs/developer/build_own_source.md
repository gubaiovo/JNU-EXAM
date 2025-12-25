# 搭建新的下载源

基础准备：

- 一个有公网 ip 的服务器
- 一个存储服务器(可选)
- 域名(可选)

## 1. 公网 IP

如果你的公网 ip 是固定的，那么可以跳过此步
如果不是固定的，你需要准备一个域名，并在你的服务器上安装 ddns 服务，推荐使用 ddns-go: https://github.com/jeessy2/ddns-go
绑定好 ddns 服务后，进行下一步

## 2. 选择存储方式

有两种存储方式：

1. 在你的服务器进行本地存储
2. 选择市面上的存储服务，比如蓝奏云、Cloudflare R2 等

### 2.1 本地存储

#### 2.1.1 获取资料，搭建访问服务

首先需要将资料存到本地：

```bash
git clone https://github.com/gubaiovo/JNU-EXAM.git
```

选择访问方式：

1. 使用简单的 http 服务
2. 使用对象存储

对于第一种方式，只需要用 python 开启简单 http 服务即可：

```bash
python -m http.server
```

对于第二种，推荐使用 RustFS 项目搭建对象存储服务：https://rustfs.com.cn/

#### 2.1.2 生成源列表和文件索引列表{#2.1.2}

`source_list`格式如下：

```json
{
    "Github": {
        "json_url": "https://github.com/gubaiovo/JNU-EXAM/raw/main/directory_structure.json",
        "file_key": "github_raw_url"
    },
    "Cloudflare R2": {
        "json_url": "https://jnuexam.xyz/directory_structure.json",
        "file_key": "cf_url"
    },
}
```

以 Github 源为例：

- `"Github"`: **源名称**
- `json_url`: **文件索引链接**
- `file_key`: **在索引文件中，文件下载链接的键值**

文件索引通过脚本生成：https://github.com/gubaiovo/DirTreeJson
文件索引脚本中，全局变量`SOURCE`定义了索引文件中包含的源

```python
SOURCES = [
    {
        "name": "Github",
        "key": "github_raw_url",
        "base": "https://raw.githubusercontent.com/gubaiovo/JNU-EXAM/main",
        "type": "tree",
        "enabled": True
    },
    {
        "name": "Gitee",
        "key": "gitee_raw_url",
        "base": "https://gitee.com/gubaiovo/jnu-exam/raw/main",
        "type": "tree",
        "enabled": False
    }
]
```

- `name`: 源名称
- `key`: 文件下载链接的键值，需要与`source_list`中`file_key`相同
- `type`: 包含两种方式
  - `tree`: 以真实的文件树形式
  - `flat`: 对于有文件夹层级限制的存储服务，需要减少文件夹层级次数。脚本会去除路径中的特殊符号，用 `__` 代替文件夹层级
- `enabled`: 是否启用这个源，如果为 `False`，那么生成的索引文件不会包含这个源

你需要修改文件索引脚本来匹配你的存储服务。你的脚本中`SOURCES`的`key`需要与`source_list`中的`file_key`一致

### 2.2 通过存储服务存储

#### 2.2.1 上传文件

首先将所有资料下载到自己的电脑：

```bash
git clone https://github.com/gubaiovo/JNU-EXAM.git
```

打开存储服务控制面板，上传资料

#### 2.2.2

参考 [2.1.2 生成源列表和文件索引列表](#2.1.2)
