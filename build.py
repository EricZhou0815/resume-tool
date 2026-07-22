#!/usr/bin/env python3
"""
简历构建工具 — 把 config.md 渲染成 HTML

用法:
  python3 build.py                   # 生成简历 HTML
  python3 build.py --watch           # 监听 config 变化自动刷新
  python3 build.py --pdf             # 生成 HTML 后打开浏览器打印
"""
import re, json, os, sys
from pathlib import Path

BASE = Path.home() / "resume-tool"

def parse_config(path: Path) -> dict:
    """解析 config.md 的 frontmatter + body"""
    text = path.read_text()
    
    # 解析 frontmatter (--- 之间的 YAML-like 内容)
    fm_match = re.match(r'^---\n(.+?)\n---\n', text, re.DOTALL)
    config = {}
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.strip().split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                config[key.strip()] = val.strip().strip('"').strip("'")
    
    # 解析 body (Markdown 内容)
    body = text[fm_match.end():] if fm_match else text
    
    # 把 Markdown body 转成 HTML 片段
    html_body = markdown_to_html(body)
    config['content'] = html_body
    config['body_raw'] = body
    
    return config

def markdown_to_html(md: str) -> str:
    """简单地把 Markdown 转成 HTML（够简历用）"""
    html = []
    lines = md.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # ## Section Title
        if line.startswith('## '):
            html.append(f'<div class="section"><h2>{line[3:]}</h2>')
            # 收集后面的内容直到下一个 ##
            i += 1
            content_lines = []
            while i < len(lines) and not lines[i].startswith('## '):
                content_lines.append(lines[i])
                i += 1
            html.append(parse_section_content('\n'.join(content_lines)))
            html.append('</div>')
            continue
        
        # ### Sub Title
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
        
        # 其他行暂不处理
        i += 1
    
    return '\n'.join(html)

def parse_section_content(text: str) -> str:
    """解析 section 内的内容"""
    html = []
    lines = text.strip().split('\n')
    i = 0
    in_list = False
    in_tags = False
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            if in_list: html.append('</ul>'); in_list = False
            if in_tags: html.append('</div>'); in_tags = False
            i += 1
            continue
        
        # Skills (以 - ** 开头)
        if line.startswith('- **') and ':**' in line:
            if not in_tags:
                if in_list: html.append('</ul>'); in_list = False
            # 提取技能标签
            parts = line.split(':**')
            tags_text = parts[1].strip() if len(parts) > 1 else ''
            tags = [t.strip() for t in tags_text.split(',')]
            if not in_tags:
                html.append('<div class="skills-tags">')
                in_tags = True
            for tag in tags:
                html.append(f'<span>{tag}</span>')
        
        # List item
        elif line.startswith('- '):
            if in_tags: html.append('</div>'); in_tags = False
            if not in_list:
                html.append('<ul>')
                in_list = True
            text = line[2:]
            # Bold for **text**
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            # Italic for *text*
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            # Link [text](url)
            text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
            html.append(f'<li>{text}</li>')
        
        # 普通段落（日期、公司名等）
        else:
            if in_list: html.append('</ul>'); in_list = False
            if in_tags: html.append('</div>'); in_tags = False
            text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
            text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
            html.append(f'<p class="meta">{text}</p>')
        
        i += 1
    
    if in_list: html.append('</ul>')
    if in_tags: html.append('</div>')
    
    return '\n'.join(html)

def render(config: dict) -> str:
    """用 config 填充模板"""
    template_path = BASE / "templates" / f"{config.get('template', 'modern')}.html"
    if not template_path.exists():
        template_path = BASE / "templates" / "modern.html"
    
    html = template_path.read_text()
    
    # 替换占位符
    for key, val in config.items():
        placeholder = f'{{{{{key}}}}}'
        if placeholder in html:
            html = html.replace(placeholder, str(val))
    
    return html

def save(html: str, name: str = "resume"):
    output_path = BASE / "output" / f"{name}.html"
    output_path.write_text(html)
    return output_path

def main():
    config_path = BASE / "config.md"
    if not config_path.exists():
        print("❌ config.md 不存在")
        return
    
    config = parse_config(config_path)
    html = render(config)
    path = save(html, "resume")
    
    print(f"✅ 简历已生成: {path}")
    print(f"   打开方式: open {path}")

if __name__ == "__main__":
    main()
