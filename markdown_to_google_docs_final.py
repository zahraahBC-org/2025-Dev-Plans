#!/usr/bin/env python3
"""
Markdown to Google Docs - Final Solution with Inline Styles
محول Markdown إلى Google Docs - الحل النهائي مع Inline Styles

Version: 6.0 - Professional with Syntax Highlighting
Created: 2025-10-19

المميزات:
✅ Inline styles (Google Docs compatible)
✅ Syntax highlighting للكلمات المفتاحية
✅ Indentation محفوظة بـ &nbsp;
✅ خلفية بيضاء (لا رمادي)
✅ Code colors احترافية (VS Code theme)
✅ جداول منظمة مع أرقام أسطر

Languages supported:
✅ PHP, JavaScript, Python, YAML, Bash
"""

import os
import re
from pathlib import Path
from datetime import datetime

class GoogleDocsInlineConverter:
    """محول مع inline styles لـ Google Docs"""
    
    def __init__(self):
        # الكلمات المفتاحية للغات مختلفة
        self.keywords = {
            'php': ['<?php', '<?', '?>', 'namespace', 'use', 'class', 'function', 'public', 'private', 
                    'protected', 'return', 'if', 'else', 'foreach', 'while', 'for', 'new', 'extends',
                    'implements', 'static', 'const', 'var', 'array', 'true', 'false', 'null'],
            'javascript': ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while',
                          'class', 'extends', 'import', 'export', 'from', 'async', 'await', 'try',
                          'catch', 'throw', 'new', 'this', 'super', 'true', 'false', 'null'],
            'python': ['def', 'class', 'return', 'if', 'else', 'elif', 'for', 'while', 'import',
                      'from', 'try', 'except', 'finally', 'with', 'as', 'pass', 'break', 'continue',
                      'True', 'False', 'None', 'self', 'lambda', 'yield'],
            'yaml': ['true', 'false', 'null', 'yes', 'no'],
            'bash': ['echo', 'cd', 'ls', 'mkdir', 'rm', 'chmod', 'sudo', 'export', 'if', 'then', 'fi']
        }
    
    def highlight_syntax(self, code, lang='text'):
        """إضافة syntax highlighting للكود"""
        if lang.lower() not in self.keywords:
            return code
        
        keywords = self.keywords[lang.lower()]
        
        # تلوين الكلمات المفتاحية
        for keyword in keywords:
            # Pattern للكلمة كاملة فقط
            pattern = r'\b' + re.escape(keyword) + r'\b'
            replacement = f'<span style="color:#c678dd;font-weight:bold;">{keyword}</span>'
            code = re.sub(pattern, replacement, code)
        
        # تلوين Strings
        # Single quotes
        code = re.sub(r"'([^']*)'", r"<span style='color:#98c379;'>'&lt;span style='color:#98c379;'&gt;\1&lt;/span&gt;'</span>", code)
        # Double quotes
        code = re.sub(r'"([^"]*)"', r'<span style="color:#98c379;">"&lt;span style="color:#98c379;"&gt;\1&lt;/span&gt;"</span>', code)
        
        # تلوين Comments
        if lang.lower() in ['php', 'javascript', 'java', 'c', 'cpp']:
            code = re.sub(r'//(.*)$', r'<span style="color:#5c6370;font-style:italic;">//\1</span>', code, flags=re.MULTILINE)
        if lang.lower() == 'python':
            code = re.sub(r'#(.*)$', r'<span style="color:#5c6370;font-style:italic;">#\1</span>', code, flags=re.MULTILINE)
        
        return code
    
    def convert_code_block_to_table(self, code, lang='text'):
        """تحويل Code Block إلى جدول مع syntax highlighting"""
        lines = code.strip().split('\n')
        
        # جدول مع inline styles
        table_html = '<div style="width:100%;max-width:100%;overflow-x:auto;margin:1em 0;">'
        table_html += '<table style="width:100%;border-collapse:collapse;background:#282c34;font-family:Consolas,monospace;font-size:10pt;color:#abb2bf;direction:ltr;text-align:left;border:2px solid #3b82f6;table-layout:auto;">'
        
        for i, line in enumerate(lines, 1):
            # حفظ المسافات في البداية
            leading_spaces = len(line) - len(line.lstrip(' '))
            indentation = '&nbsp;' * leading_spaces
            line_content = line.lstrip(' ')
            
            # Escape HTML أولاً
            line_content = line_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Apply syntax highlighting
            if lang.lower() in self.keywords:
                # تلوين الكلمات المفتاحية
                for keyword in self.keywords[lang.lower()]:
                    if keyword in ['&lt;?php', '&lt;?', '?&gt;']:
                        pattern = re.escape(keyword)
                        replacement = f'<span style="color:#c678dd;font-weight:bold;">{keyword}</span>'
                        line_content = re.sub(pattern, replacement, line_content)
                    else:
                        # تأكد من البحث عن الكلمة الكاملة
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        replacement = f'<span style="color:#c678dd;font-weight:bold;">{keyword}</span>'
                        line_content = re.sub(pattern, replacement, line_content)
                
                # تلوين Strings
                line_content = re.sub(r"'([^']*)'", r"<span style='color:#98c379;'>'<span style='color:#98c379;'>\1</span>'</span>", line_content)
                line_content = re.sub(r'&quot;([^&]*)&quot;', r"<span style='color:#98c379;'>&quot;<span style='color:#98c379;'>\1</span>&quot;</span>", line_content)
                
                # تلوين الأقواس
                line_content = re.sub(r'\(', r'<span style="color:#e5c07b;">(</span>', line_content)
                line_content = re.sub(r'\)', r'<span style="color:#e5c07b;">)</span>', line_content)
                line_content = re.sub(r'\{', r'<span style="color:#e5c07b;">{</span>', line_content)
                line_content = re.sub(r'\}', r'<span style="color:#e5c07b;">}</span>', line_content)
                line_content = re.sub(r'\[', r'<span style="color:#e5c07b;">[</span>', line_content)
                line_content = re.sub(r'\]', r'<span style="color:#e5c07b;">]</span>', line_content)
                
                # تلوين الأسهم
                line_content = re.sub(r'=&gt;', r'<span style="color:#56b6c2;">=&gt;</span>', line_content)
                line_content = re.sub(r'-&gt;', r'<span style="color:#56b6c2;">-&gt;</span>', line_content)
            
            # دمج indentation مع المحتوى
            final_line = indentation + line_content if line_content else "&nbsp;"
            
            table_html += '<tr style="background:#282c34;">'
            # عمود رقم السطر
            table_html += f'<td style="background:#21252b;color:#5c6370;text-align:right;padding:4px 8px;border:none;width:40px;min-width:40px;font-family:Consolas,monospace;direction:ltr;vertical-align:top;">{i}</td>'
            # عمود الكود
            table_html += f'<td style="padding:4px 12px;border:none;white-space:normal;font-family:Consolas,monospace;color:#abb2bf;direction:ltr;text-align:left;">{final_line}</td>'
            table_html += '</tr>'
        
        table_html += '</table></div>'
        
        return table_html
    
    def convert_markdown_table(self, table_text):
        """تحويل جدول Markdown إلى HTML table"""
        lines = [line.strip() for line in table_text.strip().split('\n') if line.strip()]
        
        if len(lines) < 3:
            return table_text
        
        # السطر الأول: العناوين
        headers = [cell.strip() for cell in lines[0].split('|') if cell.strip()]
        
        # السطر الثاني: الفواصل (نتجاهله)
        
        # باقي الأسطر: البيانات
        data_rows = []
        for line in lines[2:]:
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if cells and len(cells) > 0:
                data_rows.append(cells)
        
        # إنشاء جدول HTML مع inline styles - حجم خط 10pt
        table_html = '<table style="width:100%;border-collapse:collapse;margin:1em 0;font-size:10pt;">'
        
        # Headers
        table_html += '<thead><tr>'
        for header in headers:
            table_html += f'<th style="background:#3b82f6;color:white;font-weight:bold;border:1px solid #e2e8f0;padding:8px 10px;text-align:center;font-size:10pt;">{header}</th>'
        table_html += '</tr></thead>'
        
        # Data rows
        table_html += '<tbody>'
        for i, row in enumerate(data_rows):
            bg_color = '#f8fafc' if i % 2 == 0 else 'white'
            table_html += f'<tr style="background:{bg_color};">'
            for cell in row:
                table_html += f'<td style="border:1px solid #e2e8f0;padding:6px 10px;text-align:right;font-size:10pt;">{cell}</td>'
            table_html += '</tr>'
        table_html += '</tbody>'
        
        table_html += '</table>'
        
        return table_html
    
    def convert_markdown_to_html(self, markdown_content, filename="document"):
        """تحويل Markdown إلى HTML مع inline styles"""
        html = markdown_content
        
        # Convert markdown tables FIRST (قبل أي شيء)
        def table_replace(match):
            return self.convert_markdown_table(match.group(0))
        
        # Pattern للجداول Markdown
        table_pattern = r'^\|.+\|[ ]*\n\|[-:\s|]+\|[ ]*\n(?:\|.+\|[ ]*\n?)+'
        html = re.sub(table_pattern, table_replace, html, flags=re.MULTILINE)
        
        # Convert code blocks SECOND
        def code_block_replace(match):
            lang = match.group(1) or 'text'
            code = match.group(2)
            return self.convert_code_block_to_table(code, lang)
        
        html = re.sub(r'```(\w+)?\n(.*?)```', code_block_replace, html, flags=re.DOTALL)
        
        # Convert headers with inline styles
        # H1 - مع inline styles كاملة
        html = re.sub(r'^# (.+)$', 
            r'<h1 style="font-size:16pt;font-weight:bold;color:#2563eb;border-bottom:2px solid #3b82f6;padding-bottom:0.3em;margin:0;margin-bottom:1em;display:block;">\1</h1>', 
            html, flags=re.MULTILINE)
        
        # H2 - مع inline styles + سطر فارغ قبله
        html = re.sub(r'^## (.+)$', 
            r'<p style="margin:0;padding:0;line-height:0.1;"> </p><h2 style="font-size:13pt;font-weight:bold;color:#1e40af;border-bottom:1px solid #60a5fa;padding-bottom:0.2em;margin-top:1em;margin-bottom:0.5em;display:block;">\1</h2>', 
            html, flags=re.MULTILINE)
        
        # H3 - مع inline styles + سطر فارغ قبله
        html = re.sub(r'^### (.+)$', 
            r'<p style="margin:0;padding:0;line-height:0.1;"> </p><h3 style="font-size:11pt;font-weight:bold;color:#1e3a8a;margin-top:0.8em;margin-bottom:0.5em;display:block;">\1</h3>', 
            html, flags=re.MULTILINE)
        
        # H4/H5 - مع inline styles
        html = re.sub(r'^#### (.+)$', 
            r'<h4 style="font-size:11pt;font-weight:bold;color:#1e293b;margin-top:0.5em;margin-bottom:0.5em;">\1</h4>', 
            html, flags=re.MULTILINE)
        
        # Convert inline code
        html = re.sub(r'`([^`]+)`', 
            r'<code style="background:#f1f5f9;padding:2px 6px;border-radius:3px;font-family:Consolas,monospace;color:#dc2626;font-size:10pt;direction:ltr;border:1px solid #e2e8f0;">\1</code>', 
            html)
        
        # Convert bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(?!\*)(.+?)\*', r'<em>\1</em>', html)
        
        # Convert links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', 
            r'<a href="\2" style="color:#2563eb;text-decoration:none;">\1</a>', 
            html)
        
        # Convert checkboxes
        html = re.sub(r'^- \[x\] (.+)$', 
            r'<li style="list-style-type:none;margin:0.3em 0;"><span style="color:#10b981;font-weight:bold;">✅</span> \1</li>', 
            html, flags=re.MULTILINE)
        html = re.sub(r'^- \[ \] (.+)$', 
            r'<li style="list-style-type:none;margin:0.3em 0;"><span style="color:#ef4444;font-weight:bold;">☐</span> \1</li>', 
            html, flags=re.MULTILINE)
        
        # Convert unordered lists
        html = re.sub(r'^- (.+)$', 
            r'<li style="margin:0.2em 0;">\1</li>', 
            html, flags=re.MULTILINE)
        
        # Convert ordered lists
        html = re.sub(r'^\d+\. (.+)$', 
            r'<li style="margin:0.2em 0;">\1</li>', 
            html, flags=re.MULTILINE)
        
        # Wrap list items
        def wrap_list_items(text):
            # Unordered lists
            pattern_ul = r'(<li style="margin:0\.2em 0;">.*?</li>\s*)+'
            def wrap_ul(match):
                items = match.group(0)
                return f'<ul style="font-size:11pt;margin:0.5em 0;padding-right:2em;line-height:1.15;">\n{items}</ul>\n'
            text = re.sub(pattern_ul, wrap_ul, text, flags=re.DOTALL)
            
            # Checkbox items
            pattern_cb = r'(<li style="list-style-type:none;margin:0\.3em 0;">.*?</li>\s*)+'
            def wrap_cb(match):
                items = match.group(0)
                return f'<ul style="font-size:11pt;margin:0.5em 0;padding-right:2em;list-style-type:none;">\n{items}</ul>\n'
            text = re.sub(pattern_cb, wrap_cb, text, flags=re.DOTALL)
            
            return text
        
        html = wrap_list_items(html)
        
        # Convert horizontal rules
        html = re.sub(r'^---+$', 
            r'<hr style="border:none;height:2px;background:linear-gradient(90deg,transparent,#3b82f6,transparent);margin:2em 0;">', 
            html, flags=re.MULTILINE)
        
        # Convert paragraphs
        lines = html.split('\n')
        processed_lines = []
        in_table = False
        
        for line in lines:
            if '<table' in line:
                in_table = True
            if '</table>' in line:
                if in_table:
                    in_table = False
                processed_lines.append(line)
                continue
            
            if in_table:
                processed_lines.append(line)
                continue
            
            if line.strip() and not re.match(r'^<[^>]+>', line):
                processed_lines.append(f'<p style="font-size:11pt;margin:0.3em 0;line-height:1.15;">{line}</p>')
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def create_full_html(self, content, title="Document"):
        """إنشاء HTML كامل مع minimal CSS"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # CSS بسيط جداً - فقط للعرض في المتصفح
        minimal_css = """
        <style>
            @page { size: A4 portrait; margin: 2.5cm; }
            body { 
                font-family: 'IBM Plex Sans Arabic', Cairo, Calibri, Arial, sans-serif;
                max-width: 100%;
                margin: 0 auto;
                padding: 20px;
                direction: rtl;
                text-align: right;
                background: white;  /* إصلاح: خلفية بيضاء */
            }
            .container {
                background: white;
                padding: 40px;
                max-width: 100%;
            }
        </style>
        """
        
        return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {minimal_css}
</head>
<body>
    <div class="container">
        {content}
        <p style="margin-top:2em;padding-top:1em;border-top:1px solid #e2e8f0;color:#64748b;font-size:9pt;">
            <strong>المستند:</strong> {title} | <strong>التاريخ:</strong> {current_date}
        </p>
    </div>
</body>
</html>"""
    
    def convert_file(self, input_file, output_file=None):
        """تحويل ملف"""
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        filename = Path(input_file).stem
        html_content = self.convert_markdown_to_html(markdown_content, filename)
        full_html = self.create_full_html(html_content, filename)
        
        if output_file is None:
            output_file = str(Path(input_file).with_suffix('.html'))
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        return output_file
    
    def merge_folder_to_single_file(self, folder_path, output_file=None):
        """دمج جميع ملفات MD في مجلد إلى ملف HTML واحد"""
        
        print(f"📁 دمج مجلد | Merging folder:")
        print(f"   {folder_path}\n")
        
        # البحث عن جميع ملفات .md
        md_files = sorted(list(Path(folder_path).rglob('*.md')))
        
        if not md_files:
            print("❌ لا توجد ملفات .md في المجلد")
            return None
        
        print(f"📊 عدد الملفات | Files found: {len(md_files)}\n")
        
        merged_content = []
        
        for i, md_file in enumerate(md_files, 1):
            print(f"[{i}/{len(md_files)}] معالجة | Processing: {md_file.name}")
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                # إضافة فاصل بين الملفات
                if i > 1:
                    merged_content.append('<hr style="border:none;height:3px;background:#3b82f6;margin:3em 0;">')
                    merged_content.append('<div style="page-break-before:always;"></div>')
                
                # إضافة عنوان الملف
                file_title = f'<div style="text-align:center;padding:1.5em;background:#f0f9ff;border:2px solid #3b82f6;border-radius:8px;margin:2em 0;">'
                file_title += f'<h2 style="font-size:14pt;font-weight:bold;color:#2563eb;margin:0;">📄 {md_file.name}</h2>'
                file_title += f'<p style="font-size:9pt;color:#64748b;margin:0.5em 0 0 0;">المسار: {md_file.relative_to(folder_path)}</p>'
                file_title += '</div>'
                merged_content.append(file_title)
                
                # تحويل المحتوى
                html_content = self.convert_markdown_to_html(markdown_content, md_file.stem)
                merged_content.append(html_content)
                
            except Exception as e:
                print(f"   ❌ خطأ | Error: {str(e)}")
        
        # إنشاء ملف الإخراج
        if output_file is None:
            folder_name = Path(folder_path).name
            output_file = Path(folder_path).parent / f"{folder_name}_MERGED.html"
        
        # دمج المحتوى
        final_content = '\n'.join(merged_content)
        full_html = self.create_full_html(final_content, f"Merged: {Path(folder_path).name}")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"\n✅ تم الدمج بنجاح! | Merge successful!")
        print(f"📁 الملف المدمج | Merged file:")
        print(f"   {output_file}\n")
        
        return str(output_file)
    
    def convert_folder_preserve_structure(self, folder_path, output_folder_name="html_output"):
        """تحويل جميع ملفات MD مع الحفاظ على الهيكل"""
        
        folder_path = Path(folder_path)
        output_base = folder_path / output_folder_name
        
        print(f"📁 تحويل مجلد كامل مع الحفاظ على الهيكل | Converting folder with structure preservation")
        print(f"   المصدر | Source: {folder_path}")
        print(f"   الهدف | Output: {output_base}")
        print()
        
        # إنشاء المجلد الرئيسي للإخراج
        output_base.mkdir(exist_ok=True)
        
        # البحث عن جميع ملفات .md
        md_files = sorted(list(folder_path.rglob('*.md')))
        
        if not md_files:
            print("❌ لا توجد ملفات .md في المجلد")
            return None
        
        print(f"📊 عدد الملفات | Files found: {len(md_files)}\n")
        
        converted_count = 0
        failed_count = 0
        
        for i, md_file in enumerate(md_files, 1):
            # تخطي ملفات معينة إذا لزم الأمر
            if md_file.name.startswith('.'):
                continue
            
            try:
                # حساب المسار النسبي
                relative_path = md_file.relative_to(folder_path)
                
                # إنشاء نفس الهيكل في مجلد الإخراج
                output_file = output_base / relative_path.with_suffix('.html')
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                # عرض التقدم
                print(f"[{i}/{len(md_files)}] {relative_path}")
                
                # التحويل
                with open(md_file, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                html_content = self.convert_markdown_to_html(markdown_content, md_file.stem)
                full_html = self.create_full_html(html_content, md_file.stem)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                converted_count += 1
                
            except Exception as e:
                print(f"   ❌ خطأ | Error: {str(e)}")
                failed_count += 1
        
        print()
        print("=" * 70)
        print("📊 الإحصائيات | Statistics:")
        print("=" * 70)
        print(f"✅ تم تحويلها | Converted: {converted_count}")
        print(f"❌ فشل | Failed: {failed_count}")
        print(f"📁 المجلد الناتج | Output folder: {output_base}")
        print("=" * 70)
        print()
        
        return str(output_base)


def main():
    """البرنامج الرئيسي"""
    
    print("=" * 70)
    print("🚀 المحول النهائي لـ Google Docs - Professional Edition")
    print("   Final Google Docs Converter - v6.0")
    print("=" * 70)
    print()
    print("✨ المميزات | Features:")
    print("   ✅ Syntax highlighting احترافي")
    print("   ✅ Indentation محفوظة")
    print("   ✅ العناوين bold تلقائياً")
    print("   ✅ خلفية بيضاء نظيفة")
    print("=" * 70)
    print()
    
    converter = GoogleDocsInlineConverter()
    
    # اختر الوضع
    print("اختر وضع التحويل | Select mode:")
    print()
    print("1️⃣  تحويل ملف واحد | Convert single file")
    print("2️⃣  دمج مجلد في ملف واحد | Merge folder to single file")
    print("3️⃣  تحويل مجلد مع الحفاظ على الهيكل | Convert folder preserving structure")
    print()
    
    mode = input("اختيارك | Your choice (1, 2, or 3): ").strip()
    print()
    
    if mode == '1':
        # تحويل ملف واحد
        print("📝 أدخل مسار ملف Markdown | Enter Markdown file path:")
        print("   مثال | Example: /Users/ZahraahIT/Documents/Zahraah/2025-Plans/APIs_v2/README.md")
        print()
        
        input_path = input("📄 المسار | Path: ").strip().strip('"').strip("'")
        
        if not os.path.exists(input_path):
            print(f"\n❌ الملف غير موجود | File not found: {input_path}")
            return
        
        if not os.path.isfile(input_path):
            print(f"\n❌ المسار ليس ملف | Path is not a file: {input_path}")
            return
        
        print()
        print(f"📄 معالجة الملف | Processing file:")
        print(f"   {input_path}")
        print()
        
        try:
            output_file = converter.convert_file(input_path)
            
            print("✅ تم التحويل بنجاح! | Conversion successful!")
            print()
            print(f"📁 الملف الناتج | Output file:")
            print(f"   {output_file}")
            print()
            
        except Exception as e:
            print(f"❌ خطأ في التحويل | Error: {str(e)}")
            return
    
    elif mode == '2':
        # دمج مجلد
        print("📁 أدخل مسار المجلد | Enter folder path:")
        print("   مثال | Example: /Users/ZahraahIT/Documents/Zahraah/2025-Plans/APIs_v2")
        print()
        
        input_path = input("📁 المسار | Path: ").strip().strip('"').strip("'")
        
        if not os.path.exists(input_path):
            print(f"\n❌ المجلد غير موجود | Folder not found: {input_path}")
            return
        
        if not os.path.isdir(input_path):
            print(f"\n❌ المسار ليس مجلد | Path is not a folder: {input_path}")
            return
        
        print()
        
        try:
            output_file = converter.merge_folder_to_single_file(input_path)
            
            if output_file:
                print("=" * 70)
                print("📊 الإحصائيات | Statistics:")
                print("=" * 70)
                
                # حساب حجم الملف
                file_size = os.path.getsize(output_file) / 1024  # KB
                print(f"📦 حجم الملف | File size: {file_size:.2f} KB")
                print()
        
        except Exception as e:
            print(f"❌ خطأ في الدمج | Error: {str(e)}")
            return
    
    elif mode == '3':
        # تحويل مجلد مع الحفاظ على الهيكل
        print("📁 أدخل مسار المجلد | Enter folder path:")
        print("   مثال | Example: /Users/ZahraahIT/Documents/Zahraah/2025-Plans/APIs_v2")
        print()
        
        input_path = input("📁 المسار | Path: ").strip().strip('"').strip("'")
        
        if not os.path.exists(input_path):
            print(f"\n❌ المجلد غير موجود | Folder not found: {input_path}")
            return
        
        if not os.path.isdir(input_path):
            print(f"\n❌ المسار ليس مجلد | Path is not a folder: {input_path}")
            return
        
        print()
        print("📝 أدخل اسم مجلد الإخراج | Enter output folder name:")
        print("   (افتراضي | default: APIs_v2_html)")
        print()
        
        output_name = input("📁 الاسم | Name (press Enter for default): ").strip() or "APIs_v2_html"
        
        print()
        
        try:
            output_folder = converter.convert_folder_preserve_structure(input_path, output_name)
            
            if output_folder:
                print("=" * 70)
                print("✅ اكتمل التحويل! | Conversion complete!")
                print("=" * 70)
        
        except Exception as e:
            print(f"❌ خطأ في التحويل | Error: {str(e)}")
            return
    
    else:
        print("❌ اختيار غير صحيح | Invalid choice")
        return
    
    # تعليمات الاستيراد
    print("=" * 70)
    print("📋 خطوات الاستيراد إلى Google Docs:")
    print("=" * 70)
    print()
    print("1️⃣  اذهب إلى drive.google.com")
    print("2️⃣  اسحب الملف .html وأفلته")
    print("3️⃣  انقر بالزر الأيمن → Open with → Google Docs")
    print("4️⃣  ✨ جميع التنسيقات ستظهر صحيحة!")
    print()
    print("⚠️  ملاحظة مهمة | Important note:")
    print("    عرض الجداول يحتاج ضبط يدوي:")
    print("    Format → Table → Table properties → Width: 100%")
    print()
    print("💡 أو: نسخ ولصق من المتصفح")
    print("   Cmd+A → Cmd+C → Google Docs → Cmd+V")
    print()


if __name__ == "__main__":
    main()

