# 怎么用下载器

## 获取下载器  
Web 端下载器直接访问 [https://jnuexam.gubaiovo.com/download/index.html](https://jnuexam.gubaiovo.com/download/index.html) 即可使用。  
对于电脑端和手机端，可以到 QQ 群 `757343447` 群文件获取。  
对于电脑下载器，可以到 [Github Releases](https://github.com/gubaiovo/JNU-EXAM-Downloader/releases) 页面下载。如果不知道怎么在Github Releases 页面下载，也可以到 [下载 JNU-EXAM-Downloader](https://jnuexam.gubaiovo.com/download/getapp.html) 页面下载。  

## 使用下载器

建议在使用前，先了解下载器的基本工作流程，这将帮助您更顺利地找到所需文件。整个过程主要分为以下三步：

1. 查看下载源
2. 选择下载源
3. 选择并下载文件

> 详细技术流程说明（可跳过）  
> 若您想了解其背后的工作原理，可以参考以下说明：
> 
> - 第一步：下载器会从指定的服务器获取一个名为 `source_list` 的文件，该文件包含了所有可用的下载源（也称为`仓库`）。下载器解析后会展示这些下载源。
> - 第二步：当您选择一个下载源后，下载器会从该源获取名为 `directory_structure` 的文件列表（也称为`索引`），其中列出了该源内所有文件的名称及其对应的下载链接，并展示出来。
> - 第三步：从列表中选择目标文件，下载器即会访问对应的链接并开始下载。

## 1. 查看下载源

下载器默认从 [Vercel](https://www.gubaiovo.com/jnu-exam/source_list.json) 获取下载源列表，此源较为稳定。

您也可以根据需要，在下载器中手动更换获取下载源列表的链接（URL）：

- 在安卓端，更换位置位于：`设置`->`更换源`
- 在电脑端，更换位置位于：`右上角齿轮`

下面提供了一些公开的获取下载源的链接(url)：

1. Vercel（新版默认）：`https://jnuexam.gubaiovo.com/source_list.json`  
2. Vercel（停用）：`https://www.gubaiovo.com/jnu-exam/source_list.json`    
3. Cloudflare R2: `https://jnuexam.xyz/source_list.json`  
4. Floating提供: `https://jnuexam.142751.xyz/source_list.json`  
5. Cloudflare R2 测试: `https://jnuexamfile.gubaiovo.com/source_list.json`  

## 2. 选择下载源

获取下载源列表后，您需要从中选择一个来查看其中的文件。

- 在安卓端，选择位置位于：`设置`->`更换仓库`
- 在电脑端，更换位置位于：`左上角选择框`

## 3. 选择并下载文件

完成上述两步后，下载器将显示您所选下载源中的完整文件列表。此时，您可以直接点击列表中的任意文件开始下载。