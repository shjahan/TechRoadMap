# PowerShell script to convert all markdown files to PDF
# Requires pandoc to be installed

Write-Host "Starting conversion of markdown files to PDF..." -ForegroundColor Green

# Check if pandoc is installed
try {
    $pandocVersion = pandoc --version
    Write-Host "Pandoc found: $($pandocVersion[0])" -ForegroundColor Green
} catch {
    Write-Host "Error: Pandoc is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install pandoc from: https://pandoc.org/installing.html" -ForegroundColor Yellow
    exit 1
}

# Get all markdown files in the Concurency folder
$markdownFiles = Get-ChildItem -Path "Concurency" -Filter "*.md" | Sort-Object Name

Write-Host "Found $($markdownFiles.Count) markdown files to convert" -ForegroundColor Cyan

# Convert each markdown file to PDF
foreach ($file in $markdownFiles) {
    $inputFile = $file.FullName
    $outputFile = $file.FullName -replace '\.md$', '.pdf'
    
    Write-Host "Converting: $($file.Name) -> $($file.BaseName).pdf" -ForegroundColor Yellow
    
    try {
        # Convert markdown to PDF using pandoc
        pandoc $inputFile -o $outputFile --pdf-engine=wkhtmltopdf -V geometry:margin=1in
        
        if (Test-Path $outputFile) {
            Write-Host "Successfully converted: $($file.BaseName).pdf" -ForegroundColor Green
        } else {
            Write-Host "Failed to create: $($file.BaseName).pdf" -ForegroundColor Red
        }
    } catch {
        Write-Host "Error converting $($file.Name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nConversion process completed!" -ForegroundColor Green
Write-Host "Check the Concurency folder for the generated PDF files." -ForegroundColor Cyan