@echo off
set b=%cd%
echo ===========current_path:%b%==============
@echo =======================start build=======================
python setup.py sdist build
@if %errorlevel%==0 (
@echo =======================build successful====================
) else (
call builderror.log
@echo =======================build failed=======================
)
twine upload dist/*
pause 1>nul