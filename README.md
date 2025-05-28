# 文本目录结构生成器

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

这是一个通用的 Python 脚本，可以读取一个格式化的文本文件，并根据其内容自动创建对应的目录和文件结构。

它的灵感来自于 `tree` 命令的输出，旨在简化和加速项目的初始化过程。你不再需要手动逐个创建文件夹和文件，只需在一个文本文件中以可视化的方式规划好项目结构，然后运行此脚本，即可一键生成所有必需的文件夹和空的源文件。

## 功能特点

* **可视化规划**：在一个文本文件中（如 `dic.txt`）直观地设计你的项目结构。
* **一键生成**：自动创建所有目录和空文件，告别手动操作，节省大量时间。
* **支持注释**：你可以在结构定义的旁边使用 `#` 添加注释，方便记录每个模块的用途。
* **通用性强**：适用于任何需要预先设定复杂目录结构的项目初始化场景，如Web开发、软件工程、数据科学项目等。

## 如何使用

1.  **准备环境**
    确保你的电脑已安装 Python 环境。

2.  **克隆或下载项目**
    将本项目文件（主要是 `create_dirs.py` 和 `dic.txt`）下载到本地。

3.  **定义目录结构**
    打开并编辑 `dic.txt` 文件，按照下方的示例格式定义你想要的目录和文件结构。
    * 目录以 `/` 结尾。
    * 文件直接写文件名。
    * 使用 `├──`、`└──` 和 `│` 来表示层级关系。

4.  **运行脚本**
    在你的终端或命令行中，导航到项目文件所在的目录，然后运行脚本：
    ```bash
    python create_dirs.py
    ```

5.  **完成**
    脚本将在当前目录下为你生成 `dic.txt` 中定义的完整项目结构。

## `dic.txt` 示例目录树

以下是用于生成 `ai-multimodal-hub` 项目的 `dic.txt` 文件内容示例。

```text
ai-multimodal-hub/
├── frontend/                 # Vue前端
│   ├── public/
│   │   └── media/           # 存放工具预览图片/视频
│   ├── src/
│   │   ├── assets/
│   │   │   └── theme.css
│   │   ├── components/
│   │   │   ├── Sidebar.vue
│   │   │   ├── HeaderBar.vue
│   │   │   ├── ToolCard.vue
│   │   │   └── IframeModal.vue
│   │   ├── data/
│   │   │   └── tools.json
│   │   ├── utils/
│   │   │   └── storage.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
└── backend/                  # Python Flask后端
    ├── app.py
    ├── requirements.txt
    └── config.py
```

## 许可证

该项目采用 [MIT](https://choosealicense.com/licenses/mit/) 许可证。
