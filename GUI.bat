@echo off
setlocal enabledelayedexpansion

:: Step 1: Ask user for directory
set "psCommand="(new-object -COM 'Shell.Application').BrowseForFolder(0,'Please choose a directory:',0,0).self.path""
for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "selected_directory=%%I"

if not defined selected_directory (
    echo No directory was selected.
    pause
    exit /b
)

echo You selected: %selected_directory%

:: Step 2: Set ZIP file URL
set "zip_url=https://example.com/file.zip"
set "zip_file=%selected_directory%\downloaded.zip"

echo Downloading zip file...
powershell -Command "(New-Object Net.WebClient).DownloadFile('%zip_url%', '%zip_file%')"

:: Step 3: Extract zip into selected directory
echo Extracting...
powershell -Command "Expand-Archive -Path '%zip_file%' -DestinationPath '%selected_directory%' -Force"

:: Step 4: Cleanup zip if you want
del "%zip_file%"

echo Done!
pause
