#!/usr/bin/env python3
"""
Google Docs Import Script
Converts markdown files to Google Docs format with proper structure
"""

import os
import re
from pathlib import Path

def convert_markdown_to_google_docs(markdown_file):
    """Convert markdown file to Google Docs format"""
    
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert markdown headers to Google Docs format
    content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
    
    # Convert bold text
    content = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', content)
    
    # Convert italic text
    content = re.sub(r'\*(.+?)\*', r'<i>\1</i>', content)
    
    # Convert code blocks
    content = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre>\2</pre>', content, flags=re.DOTALL)
    
    # Convert inline code
    content = re.sub(r'`(.+?)`', r'<code>\1</code>', content)
    
    # Convert lists
    content = re.sub(r'^- (.+)$', r'<li>\1</li>', content, flags=re.MULTILINE)
    
    # Convert links
    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', content)
    
    return content

def create_google_docs_structure():
    """Create the folder structure for Google Docs"""
    
    folders = [
        "00-Templates",
        "01-Architecture", 
        "02-Implementation",
        "03-Quality",
        "04-Operations",
        "05-Advanced",
        "06-Reference",
        "AI-Agent-Tools"
    ]
    
    print("📁 Google Docs Folder Structure:")
    for folder in folders:
        print(f"   📂 {folder}/")
        print(f"      📄 {folder}.docx")
    
    return folders

def generate_import_instructions():
    """Generate step-by-step import instructions"""
    
    instructions = """
🚀 Google Docs Import Instructions
================================

Method 1: Direct Upload (Recommended)
-------------------------------------
1. Open Google Drive (drive.google.com)
2. Click "New" → "File upload"
3. Select all Google_Docs_*.md files
4. Right-click each file → "Open with" → "Google Docs"
5. Google will auto-convert markdown to Google Docs format

Method 2: Manual Copy-Paste (Better Formatting)
-----------------------------------------------
1. Open each Google_Docs_*.md file in text editor
2. Copy all content (Ctrl+A, Ctrl+C)
3. Go to Google Docs → "New" → "Blank document"
4. Paste content (Ctrl+V)
5. Apply formatting:
   - Select headers → Apply Heading 1, 2, 3
   - Select Arabic text → Set RTL direction
   - Add page breaks between tabs
   - Create table of contents

Method 3: Batch Processing
--------------------------
1. Use this script to convert all files
2. Upload converted files to Google Drive
3. Open with Google Docs

Folder Organization:
-------------------
📂 00-Templates/
   📄 Google_Docs_00_Templates_Tab1.md → Tab 1: Risk Assessment
   📄 Google_Docs_00_Templates_Tab2.md → Tab 2: Quality Gates
   📄 Google_Docs_00_Templates_Tab3.md → Tab 3: Common Pitfalls
   📄 Google_Docs_00_Templates_Tab4.md → Tab 4: Success Criteria
   📄 Google_Docs_00_Templates_Tab5.md → Tab 5: Troubleshooting
   📄 Google_Docs_00_Templates_Tab6.md → Tab 6: Generic Priority
   📄 Google_Docs_00_Templates_Tab7.md → Tab 7: File-Specific Priority
   📄 Google_Docs_00_Templates_Tab8.md → Tab 8: Comprehensive Metrics

📂 01-Architecture/
   📄 Google_Docs_01_Architecture_Tab1.md → Tab 1: Architecture Overview
   📄 Google_Docs_01_Architecture_Tab2.md → Tab 2: State Management & DI
   📄 Google_Docs_01_Architecture_Tab3.md → Tab 3: Data Layer & Error Handling
   📄 Google_Docs_01_Architecture_Tab4.md → Tab 4: Domain Layer
   📄 Google_Docs_01_Architecture_Tab5.md → Tab 5: Presentation Layer
   📄 Google_Docs_01_Architecture_Tab6.md → Tab 6: Design System & Theming

📂 02-Implementation/
   📄 Google_Docs_02_Implementation_Tab1.md → Tab 1: Project Setup
   📄 Google_Docs_02_Implementation_Tab2.md → Tab 2: Testing Strategy
   📄 Google_Docs_02_Implementation_Tab3.md → Tab 3: Code Quality
   📄 Google_Docs_02_Implementation_Tab4.md → Tab 4: Git Workflow

📂 03-Quality/
   📄 Google_Docs_03_Quality_Tab1.md → Tab 1: CI/CD Pipeline
   📄 Google_Docs_03_Quality_Tab2.md → Tab 2: Performance Optimization
   📄 Google_Docs_03_Quality_Tab3.md → Tab 3: Security & Privacy
   📄 Google_Docs_03_Quality_Tab4.md → Tab 4: Monitoring & Analytics
   📄 Google_Docs_03_Quality_Tab5.md → Tab 5: Release Management

📂 04-Operations/
   📄 Google_Docs_04_Operations_Tab1.md → Tab 1: Redis Caching
   📄 Google_Docs_04_Operations_Tab2.md → Tab 2: Error Catalog
   📄 Google_Docs_04_Operations_Tab3.md → Tab 3: Performance Monitoring
   📄 Google_Docs_04_Operations_Tab4.md → Tab 4: Notifications & Deep Links
   📄 Google_Docs_04_Operations_Tab5.md → Tab 5: Business Analytics

📂 05-Advanced/
   📄 Google_Docs_05_Advanced_Tab1.md → Tab 1: Feature Flags
   📄 Google_Docs_05_Advanced_Tab2.md → Tab 2: Advanced Error Management
   📄 Google_Docs_05_Advanced_Tab3.md → Tab 3: Monitoring & Alerting
   📄 Google_Docs_05_Advanced_Tab4.md → Tab 4: Configuration Management
   📄 Google_Docs_05_Advanced_Tab5.md → Tab 5: Quality Management

📂 06-Reference/
   📄 Google_Docs_06_Reference_Tab1.md → Tab 1: Code Templates & Tools
   📄 Google_Docs_06_Reference_Tab2.md → Tab 2: Troubleshooting
   📄 Google_Docs_06_Reference_Tab3.md → Tab 3: Migration Guide
   📄 Google_Docs_06_Reference_Tab4.md → Tab 4: Checklists & Quick Reference
   📄 Google_Docs_06_Reference_Tab5.md → Tab 5: Glossary & Resources

📂 AI-Agent-Tools/
   📄 Google_Docs_AI_Agent_Tools_Tab1.md → Tab 1: AI Agent Specialization
   📄 Google_Docs_AI_Agent_Tools_Tab2.md → Tab 2: How to Use AI Agent
   📄 Google_Docs_AI_Agent_Tools_Tab3.md → Tab 3: Content Management Guide
   📄 Google_Docs_AI_Agent_Tools_Tab4.md → Tab 4: Universal Plan Review
   📄 Google_Docs_AI_Agent_Tools_Tab5.md → Tab 5: AI Agent Tools README

📄 Google_Docs_Master_Navigation.md → Master Navigation Document

Tips for Better Import:
---------------------
1. Use Method 2 (Copy-Paste) for best formatting control
2. Apply proper headings (H1, H2, H3) for structure
3. Set Arabic text to RTL direction
4. Add page breaks between tabs
5. Create table of contents for navigation
6. Use consistent fonts and formatting
7. Add bookmarks for quick navigation
8. Share with team members as needed

Quality Checklist:
-----------------
✅ All 8 main documents imported
✅ All 35 tabs properly formatted
✅ Bilingual support (Arabic | English) maintained
✅ Proper heading structure applied
✅ RTL direction set for Arabic text
✅ Page breaks added between tabs
✅ Table of contents created
✅ Cross-references working
✅ Professional formatting applied
✅ Ready for team collaboration
"""
    
    return instructions

def main():
    """Main function to run the import process"""
    
    print("🚀 Google Docs Import Assistant")
    print("=" * 50)
    
    # Create folder structure
    folders = create_google_docs_structure()
    
    # Generate instructions
    instructions = generate_import_instructions()
    
    # Save instructions to file
    with open("Google_Docs_Import_Instructions.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("\n📋 Import Instructions Generated!")
    print("📄 Saved to: Google_Docs_Import_Instructions.txt")
    print("\n🎯 Quick Start:")
    print("1. Open Google Drive (drive.google.com)")
    print("2. Upload all Google_Docs_*.md files")
    print("3. Right-click → 'Open with' → 'Google Docs'")
    print("4. Organize into folders by document type")
    print("5. Apply formatting and create table of contents")
    
    print(f"\n📊 Total Files to Import: {len([f for f in os.listdir('.') if f.startswith('Google_Docs_')])}")
    print("✅ Ready for Google Docs import!")

if __name__ == "__main__":
    main()
