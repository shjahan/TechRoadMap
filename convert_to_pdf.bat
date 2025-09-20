@echo off
echo Starting conversion of markdown files to PDF...

REM Check if pandoc is installed
pandoc --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Pandoc is not installed or not in PATH
    echo Please install pandoc from: https://pandoc.org/installing.html
    pause
    exit /b 1
)

echo Pandoc found, proceeding with conversion...

REM Convert each markdown file to PDF
for %%f in (Concurency\*.md) do (
    echo Converting: %%~nxf
    pandoc "%%f" -o "%%~dpnf.pdf" --pdf-engine=wkhtmltopdf -V geometry:margin=1in
    if exist "%%~dpnf.pdf" (
        echo ✓ Successfully converted: %%~nf.pdf
    ) else (
        echo ✗ Failed to convert: %%~nf.pdf
    )
)

echo.
echo Conversion process completed!
echo Check the Concurency folder for the generated PDF files.
pause