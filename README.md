# Resume Tool 🎯

你的个人职业管理中心。存一份工作经历数据库，随时生成定制简历。

**理念：** 一份数据源（profile.json），多份简历。改内容不改样式，换模板不改内容。

---

## 人 — 它是干嘛的

- 把你的所有工作经历、项目、技能存到一个地方（`profile.json`）
- 选模板 → 一键生成 HTML 简历
- 根据职位描述（JD）自动匹配最相关的经历
- 导出 PDF，随时投递

## 人 — 怎么用

### 1. 改内容

编辑 `profile.json`，加新经历、改描述、更新技能。结构很直观，按字段填就行。

### 2. 生成简历

```bash
python3 build.py
```

浏览器自动打开，右下角 **⬇ Download PDF** 按钮 → 打印 → 另存为 PDF。

### 3. 针对 JD 定制

把职位描述存成 `jd.txt`：

```bash
python3 build.py --jd jd.txt
```

工具会自动匹配相关经历，生成定向简历。

### 4. 按技能筛选

```bash
python3 build.py --tags python,react,aws
```

只包含有这些标签的经历和项目。

### 5. 选模板

```bash
python3 build.py --template modern
```

目前只有一个 modern 模板，后续会加更多。

### 6. 部署到线上

```bash
python3 build.py
git add -A && git commit -m "update" && git push
```

Vercel 自动部署，访问 `https://resume-tool-liart.vercel.app` 就能看到线上版。点 Download PDF 一样能导出。

---

## Agent（AI / Hermes）— 怎么用

`build.py` 支持所有参数，Agent 可以直接调：

```
python3 build.py                          # 全量简历
python3 build.py --tags python            # 筛选技能
python3 build.py --jd ~/jd.txt            # 匹配职位
python3 build.py --template modern --pdf  # 出 HTML + PDF
```

`profile.json` 是唯一的职业数据库，Agent 直接编辑它来增删改经历。格式是标准 JSON，写脚本解析或直接改都行。

**更新经历流程：**
1. 读取 `profile.json`
2. 修改对应字段（experience / projects / skills 等）
3. 写回
4. 跑 `python3 build.py` 验证效果

---

## 项目结构

```
resume-tool/
├── profile.json        ← 你的职业数据库（唯一内容源）
├── build.py            ← 构建脚本
├── templates/
│   └── modern.html     ← 简历模板（Jinja2）
├── output/
│   ├── resume.html     ← 生成的简历
│   ├── index.html      ← Vercel 入口
│   └── resume.pdf      ← 导出的 PDF
├── vercel.json         ← Vercel 部署配置
└── README.md
```

## 技术栈

Python 3 + Jinja2 + Playwright + HTML/CSS。零 Web 框架，纯静态生成。部署在 Vercel。
