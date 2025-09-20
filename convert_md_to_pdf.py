#!/usr/bin/env python3
"""
Convert all markdown files in the Concurency folder to PDF
Requires: pip install markdown weasyprint
"""

import os
import glob
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import sys

def convert_md_to_pdf(md_file_path, output_path):
    """Convert a single markdown file to PDF"""
    try:
        # Read markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html = markdown.markdown(md_content, extensions=['codehilite', 'fenced_code', 'tables'])
        
        # Add CSS styling
        css_content = """
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
        }
        h1 { font-size: 28px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { font-size: 24px; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }
        h3 { font-size: 20px; }
        h4 { font-size: 18px; }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            overflow-x: auto;
        }
        pre code {
            background-color: transparent;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        li {
            margin: 5px 0;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
        }
        """
        
        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{os.path.basename(md_file_path)}</title>
            <style>{css_content}</style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Convert HTML to PDF
        font_config = FontConfiguration()
        html_doc = HTML(string=full_html)
        css_doc = CSS(string=css_content, font_config=font_config)
        
        html_doc.write_pdf(output_path, stylesheets=[css_doc], font_config=font_config)
        
        return True
        
    except Exception as e:
        print(f"Error converting {md_file_path}: {str(e)}")
        return False

def main():
    """Main function to convert all markdown files"""
    print("Starting conversion of markdown files to PDF...")
    
    # Check if required libraries are installed
    try:
        import markdown
        import weasyprint
    except ImportError as e:
        print(f"Error: Required libraries not installed: {e}")
        print("Please install them using: pip install markdown weasyprint")
        return
    
    # Get all markdown files in the Concurency folder
    md_files = glob.glob("Concurency/*.md")
    md_files.sort()
    
    if not md_files:
        print("No markdown files found in the Concurency folder")
        return
    
    print(f"Found {len(md_files)} markdown files to convert")
    
    success_count = 0
    
    # Convert each markdown file to PDF
    for md_file in md_files:
        pdf_file = md_file.replace('.md', '.pdf')
        print(f"Converting: {os.path.basename(md_file)} -> {os.path.basename(pdf_file)}")
        
        if convert_md_to_pdf(md_file, pdf_file):
            print(f"✓ Successfully converted: {os.path.basename(pdf_file)}")
            success_count += 1
        else:
            print(f"✗ Failed to convert: {os.path.basename(md_file)}")
    
    print(f"\nConversion completed! {success_count}/{len(md_files)} files converted successfully.")
    print("Check the Concurency folder for the generated PDF files.")

if __name__ == "__main__":
    main()