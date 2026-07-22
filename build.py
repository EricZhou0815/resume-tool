#!/usr/bin/env python3
"""
简历构建工具 v2 — 从职业数据库生成定制简历

用法:
  python3 build.py                          # 默认：所有经历，modern 模板
  python3 build.py --template classic       # 选模板
  python3 build.py --tags python,nextjs     # 只包含含这些标签的经历
  python3 build.py --jd jd.txt              # 根据职位描述自动匹配经历
  python3 build.py --list-templates         # 列出可用模板
  python3 build.py --serve                  # 启动本地预览服务器
"""
import json, os, sys, re, shutil
from pathlib import Path
from datetime import datetime

BASE = Path.home() / "resume-tool"
PROFILE_PATH = BASE / "profile.json"
TEMPLATES_DIR = BASE / "templates"
OUTPUT_DIR = BASE / "output"

def load_profile() -> dict:
    with open(PROFILE_PATH) as f:
        return json.load(f)

def load_template(name: str) -> str:
    path = TEMPLATES_DIR / f"{name}.html"
    if not path.exists():
        print(f"⚠️ 模板 '{name}' 不存在，使用 modern")
        path = TEMPLATES_DIR / "modern.html"
    return path.read_text()

def list_templates():
    for f in sorted(TEMPLATES_DIR.glob("*.html")):
        print(f"  {f.stem}")

def filter_experience(profile: dict, tags: list[str] = None, jd_text: str = None) -> list:
    exps = profile.get("experience", [])
    
    if tags:
        exps = [e for e in exps if any(t.lower() in [x.lower() for x in e.get("tags", [])] for t in tags)]
    
    if jd_text:
        # 简单关键词匹配 — 后续可以加 AI
        jd_lower = jd_text.lower()
        scored = []
        for e in exps:
            score = 0
            for tag in e.get("tags", []):
                if tag.lower() in jd_lower:
                    score += 2
            for h in e.get("highlights", []):
                if h.lower() in jd_lower:
                    score += 1
            scored.append((score, e))
        scored.sort(key=lambda x: -x[0])
        exps = [e for _, e in scored if _ > 0]
        if not exps:
            exps = profile.get("experience", [])
    
    return exps

def filter_projects(profile: dict, tags: list[str] = None) -> list:
    projects = profile.get("projects", [])
    if tags:
        projects = [p for p in projects if any(t.lower() in [x.lower() for x in p.get("tech", [])] for t in tags)]
    return projects

def format_date(date_str: str) -> str:
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, "%Y-%m")
        return dt.strftime("%b %Y")
    except:
        return date_str

def build_context(profile: dict, exp_filter: list, proj_filter: list) -> dict:
    """把 profile 转成模板需要的 context"""
    p = profile["personal"]
    
    # 处理经历
    experiences = []
    for e in exp_filter:
        start = format_date(e.get("start_date", ""))
        end = format_date(e.get("end_date", "")) if e.get("end_date") else "Present"
        experiences.append({
            "company": e["company"],
            "position": e["position"],
            "period": f"{start} - {end}",
            "location": e.get("location", ""),
            "highlights": e.get("highlights", []),
        })
    
    # 处理项目
    projects = []
    for pj in proj_filter:
        projects.append({
            "name": pj["name"],
            "description": pj.get("description", ""),
            "tech": ", ".join(pj.get("tech", [])),
            "highlights": pj.get("highlights", []),
        })
    
    # 处理技能
    skill_groups = []
    for category, items in profile.get("skills", {}).items():
        skill_groups.append({
            "category": category.capitalize(),
            "skill_list": list(items)
        })
    
    return {
        "name": p["name"],
        "title": p["title"],
        "email": p.get("email", ""),
        "phone": p.get("phone", ""),
        "location": p.get("location", ""),
        "linkedin": p.get("linkedin", ""),
        "github": p.get("github", ""),
        "summary": p.get("summary", ""),
        "experiences": experiences,
        "education": profile.get("education", []),
        "skill_groups": skill_groups,
        "projects": projects,
        "languages": profile.get("languages", []),
        "year": datetime.now().strftime("%Y"),
    }

def render(template_name: str, context: dict) -> str:
    """使用 Jinja2 渲染模板"""
    from jinja2 import Environment, FileSystemLoader
    
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(f"{template_name}.html")
    return template.render(**context)

def save(html: str, name: str = "resume"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.html"
    path.write_text(html)
    return path

def main():
    import argparse
    parser = argparse.ArgumentParser(description="简历构建工具")
    parser.add_argument("--template", default="modern", help="模板名称")
    parser.add_argument("--tags", help="按标签筛选经历（逗号分隔）")
    parser.add_argument("--jd", help="职位描述文件路径，自动匹配经历")
    parser.add_argument("--list-templates", action="store_true", help="列出可用模板")
    parser.add_argument("--serve", action="store_true", help="启动预览服务器")
    parser.add_argument("--output", default="resume", help="输出文件名")
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    profile = load_profile()
    
    # 解析标签
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
    
    # 读取 JD
    jd_text = None
    if args.jd:
        jd_path = Path(args.jd)
        if jd_path.exists():
            jd_text = jd_path.read_text()
        else:
            print(f"⚠️ JD 文件不存在: {args.jd}")
    
    # 筛选经历和项目
    exp_filter = filter_experience(profile, tags, jd_text)
    proj_filter = filter_projects(profile, tags)
    
    # 构建 context
    context = build_context(profile, exp_filter, proj_filter)
    
    # 渲染
    html = render(args.template, context)
    path = save(html, args.output)
    
    # 复制到 output/index.html 方便 Vercel
    shutil.copy(path, OUTPUT_DIR / "index.html")
    
    count = len(exp_filter)
    print(f"✅ 简历已生成: {path}")
    print(f"   经历: {count} 条 | 模板: {args.template}")
    if tags:
        print(f"   标签筛选: {', '.join(tags)}")
    print(f"   打开: open {path}")

if __name__ == "__main__":
    main()
