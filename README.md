# Resume Tool 🎯

> 个人职业管理中心 / Personal Career Hub  
> 一份数据源，多份简历。改内容不改样式，换模板不改内容。  
> One data source, unlimited resumes. Change content without touching styles, swap templates without rewriting content.

---

## 📁 Project Structure

```
resume-tool/
├── profile.json         # Career database (single source of truth)
├── build.py             # CLI entry point
├── templates/
│   └── modern.html      # Resume template (Jinja2)
├── output/
│   ├── resume.html      # Generated resume
│   ├── index.html       # Vercel entry point
│   └── resume.pdf       # Exported PDF
├── vercel.json          # Vercel config
└── README.md
```

## 🧱 Tech Stack

Python 3 · Jinja2 · HTML/CSS · No web framework · Static generation · Deployed on Vercel

---

## 🤖 Agent / AI Integration

This tool is **agent-first** — designed to be driven by AI agents (Hermes, Claude Code, Codex, etc.), not just humans.

### Setup for agents

```bash
git clone https://github.com/EricZhou0815/resume-tool.git /path/to/resume-tool
pip3 install jinja2
```

### Calling from code

```python
import subprocess, json

# Build a resume
subprocess.run(["python3", "/path/to/resume-tool/build.py"])

# With filters
subprocess.run([
    "python3", "/path/to/resume-tool/build.py",
    "--tags", "aws,react",
    "--jd", "/path/to/jd.txt",
    "--pdf"
])

# Read and update the profile database
with open("/path/to/resume-tool/profile.json") as f:
    profile = json.load(f)

# Add a new experience entry
profile["experience"].append({
    "id": "exp-4",
    "company": "...",
    "position": "...",
    "start_date": "2025-01",
    "end_date": None,
    "current": True,
    "highlights": ["..."],
    "tags": ["..."]
})

with open("/path/to/resume-tool/profile.json", "w") as f:
    json.dump(profile, f, indent=2, ensure_ascii=False)

# Regenerate after updating
subprocess.run(["python3", "/path/to/resume-tool/build.py"])
```

### Hermes skill snippet

Paste this into a Hermes skill file to let your agent use resume-tool:

```yaml
name: resume-tool  
description: Resume builder — manage career database, generate tailored resumes

commands:
  - "python3 ~/resume-tool/build.py"
  - "python3 ~/resume-tool/build.py --tags <skills>"
  - "python3 ~/resume-tool/build.py --jd <file>"
  - "python3 ~/resume-tool/build.py --pdf"

data_file: ~/resume-tool/profile.json
```

---

## 📋 CLI Reference

| Command | Description |
|---------|-------------|
| `python3 build.py` | Full resume, modern template |
| `python3 build.py --template <name>` | Choose template |
| `python3 build.py --tags <a,b,c>` | Filter by skill tags |
| `python3 build.py --jd <file>` | Match experience to job description |
| `python3 build.py --pdf` | Generate HTML + export PDF |
| `python3 build.py --list-templates` | List available templates |
| `python3 build.py --output <name>` | Custom output filename |

---

## 🇬🇧 English

### What it is

A CLI tool that manages your entire career profile in one JSON file (`profile.json`) and generates tailored resumes from it. Pick a template, filter by skills, match against a job description — one command, one HTML resume.

### Installation

```bash
git clone https://github.com/EricZhou0815/resume-tool.git
cd resume-tool
pip3 install jinja2
```

### Usage

```bash
python3 build.py                              # Full resume
python3 build.py --tags python,react,aws      # Filter by skill tags
python3 build.py --jd jd.txt                  # Match against a job description
python3 build.py --template modern            # Choose a template
python3 build.py --pdf                        # Generate HTML + export PDF
python3 build.py --list-templates             # List available templates
```

Edit `profile.json` to update your career data. Run `python3 build.py` to regenerate.

### Deploy to Vercel

```bash
# 1. Fork or clone this repo to your own GitHub
# 2. Import your repo at https://vercel.com
# 3. Deploy — Vercel auto-detects static files

# After updating content locally:
python3 build.py
git add -A && git commit -m "update resume"
git push
```

Vercel auto-deploys. Click **Download PDF** on the live site → browser print → save as PDF.

> ⚠️ The demo link `resume-tool-liart.vercel.app` in this README is Eric's personal deployment.
> **Your own deployment will get its own Vercel URL** (e.g. `resume-tool-xxx.vercel.app`).
> Don't use someone else's link — deploy your own.

---

## 🇨🇳 中文

### 它是干嘛的

把你的所有工作经历、项目、技能存到一个地方（`profile.json`），选模板一键生成 HTML 简历，支持按职位描述（JD）自动匹配经历，导出 PDF 投递。

### 安装

```bash
git clone https://github.com/EricZhou0815/resume-tool.git
cd resume-tool
pip3 install jinja2
```

### 用法

```bash
python3 build.py                              # 全量简历
python3 build.py --tags python,react,aws      # 按技能筛选
python3 build.py --jd jd.txt                  # 匹配职位描述
python3 build.py --template modern            # 选模板
python3 build.py --pdf                        # 生成 HTML + PDF
python3 build.py --list-templates             # 列出可用模板
```

编辑 `profile.json` 更新你的职业数据。改完后跑 `python3 build.py` 即可。

### 部署到 Vercel

```bash
# 1. Fork 或 clone 这个仓库到你自己的 GitHub
# 2. 在 https://vercel.com 导入你的仓库
# 3. 部署即可，Vercel 会自动识别静态文件

# 本地更新内容后：
python3 build.py
git add -A && git commit -m "update resume"
git push
```

Vercel 自动部署。线上版右下角有 **Download PDF** 按钮，点它 → 浏览器打印 → 另存为 PDF。

> ⚠️ 注意：这个 README 里的演示链接 `resume-tool-liart.vercel.app` 是 Eric 个人的部署地址。
> **你自己部署后，会得到一个属于你的 Vercel 链接**（比如 `resume-tool-xxx.vercel.app`）。
> 不要直接使用别人的链接。
