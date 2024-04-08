cd /d "%~dp0"
:: 获取当前目录的完整路径
set "currentPath=%cd%"
:: 提取盘符
for %%i in ("%currentPath%") do set "drive=%%~di"
%drive%
.\Chrome\App\chrome "https://www.zhipin.com/web/geek/job-recommend" --remote-debugging-port=9222