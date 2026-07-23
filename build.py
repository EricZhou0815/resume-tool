#!/usr/bin/env python3
"""
简历构建工具 v2 — 从职业数据库生成定制简历

用法:
  python3 build.py                          # Default: all experience, modern template
  python3 build.py --template classic       # Choose a template
  python3 build.py --tags python,nextjs     # Filter by skill tags
  python3 build.py --jd jd.txt              # Match experience against a job description
  python3 build.py --list-templates         # List available templates
  python3 build.py --pdf                    # Generate HTML + export PDF
  python3 build.py --serve                  # Start local preview server
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
        print(f"⚠️ Template '{name}'  not found, using  modern")
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
        # Filter experience by tags or match against a job description
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
    """Build template context from profile"""
    p = profile["personal"]

    # Process experience entries
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

    # Process project entries
    projects = []
    for pj in proj_filter:
        projects.append({
            "name": pj["name"],
            "description": pj.get("description", ""),
            "tech": ", ".join(pj.get("tech", [])),
            "highlights": pj.get("highlights", []),
        })

    # Process skill groups
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
    """Render template with Jinja2"""
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(f"{template_name}.html")
    return template.render(**context)

def save(html: str, name: str = "resume"):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / f"{name}.html"
    path.write_text(html)
    return path

def build_switchable_page(templates_html: list, context: dict, active: str) -> str:
    """Build a page that contains all templates and switches between them via JS."""
    template_names = sorted([f.stem for f in TEMPLATES_DIR.glob("*.html")])
    
    # Build the switcher bar HTML
    switcher_buttons = ""
    for name in template_names:
        active_class = 'active' if name == active else ''
        label = name.capitalize()
        switcher_buttons += f'<button class="{active_class}" onclick="switchTemplate(\'{name}\')">{label}</button>'
    
    # Wrap each template in a div with its name as id
    template_divs = ""
    for name, html in zip(template_names, templates_html):
        display = 'block' if name == active else 'none'
        template_divs += f'<div id="template-{name}" style="display:{display}">{html}</div>\n'
    
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{context["name"]} - Resume</title>
<style>
  .global-switcher {{
    position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
    z-index: 1000; display: flex; gap: 6px;
    background: rgba(255,255,255,0.95); padding: 8px 14px;
    border-radius: 30px; box-shadow: 0 2px 16px rgba(0,0,0,0.12);
  }}
  .global-switcher button {{
    border: 1px solid #d0d0d0; background: white; padding: 7px 16px;
    border-radius: 20px; font-size: 13px; cursor: pointer; transition: 0.15s;
  }}
  .global-switcher button.active {{ background: #2563eb; color: white; border-color: #2563eb; }}
  .global-switcher button:hover:not(.active) {{ background: #f0f0f0; }}
</style>
</head>
<body>
<div class="global-switcher">
  {switcher_buttons}
</div>
{template_divs}
<script>
function switchTemplate(name) {{
  var templates = {json.dumps(template_names)};
  for (var i = 0; i < templates.length; i++) {{
    var el = document.getElementById('template-' + templates[i]);
    var btn = document.querySelectorAll('.global-switcher button')[i];
    if (templates[i] === name) {{
      el.style.display = 'block';
      btn.classList.add('active');
    }} else {{
      el.style.display = 'none';
      btn.classList.remove('active');
    }}
  }}
}}
</script>
</body>
</html>'''
    return page

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

    # Parse tags from comma-separated string
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    # Read job description from file
    jd_text = None
    if args.jd:
        jd_path = Path(args.jd)
        if jd_path.exists():
            jd_text = jd_path.read_text()
        else:
            print(f"⚠️ JD file not found: {args.jd}")

    # Filter experience and projects
    exp_filter = filter_experience(profile, tags, jd_text)
    proj_filter = filter_projects(profile, tags)

    # Build template context
    context = build_context(profile, exp_filter, proj_filter)

    # Render template
    html = render(args.template, context)
    
    # Wrap in HTML that includes all templates for client-side switching
    all_templates_html = []
    for tpl_name in sorted([f.stem for f in TEMPLATES_DIR.glob("*.html")]):
        all_templates_html.append(render(tpl_name, context))
    
    # Build a page that loads all templates and lets you switch
    page_html = build_switchable_page(all_templates_html, context, args.template)
    path = save(page_html, args.output)

    # Copy to output/index.html for Vercel entry point
    shutil.copy(path, OUTPUT_DIR / "index.html")

    count = len(exp_filter)
    print(f"✅ 简历已生成: {path}")
    print(f"   经历: {count} 条 | 模板: {args.template}")
    if tags:
        print(f"   标签筛选: {', '.join(tags)}")
    print(f"   打开: open {path}")

if __name__ == "__main__":
    main()
