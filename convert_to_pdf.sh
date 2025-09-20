#!/bin/bash

echo "Installing required Python packages..."
pip install -r requirements.txt

echo ""
echo "Converting markdown files to PDF..."
python3 convert_md_to_pdf.py

echo ""
echo "Conversion complete! Check the PDF_Output folder for the generated PDF files."