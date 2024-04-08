@echo off
setlocal EnableDelayedExpansion

%1 %2
ver|find "5.">nul&&goto :Admin
mshta vbscript:createobject("shell.application").shellexecute("%~s0","goto :Admin","","runas",1)(window.close)&goto :eof
:Admin
chcp 65001
cd /d "%~dp0"
echo %CD%
:: 获取当前目录的完整路径
set "currentPath=%cd%"

:: 提取盘符
for %%i in ("%currentPath%") do set "drive=%%~di"

%drive%
set "ChromeName=Chrome"
:: 定义要检查的环境变量和子字符串
set "VAR_TO_CHECK=%PATH%"
set "Chrome=%currentPath%\Chrome\App"
set "SUBSTRING_TO_FIND=Chrome"

:: 显示要查找的子字符串
echo 正在查找环境变量中是否包含：%SUBSTRING_TO_FIND%

:: 检查环境变量是否存在
if not defined VAR_TO_CHECK (
    echo 环境变量PATH不存在。
    goto End
)

:: 移除尾部的分号和可能的空格


:: 指定要读取的注册表项和值名
set "regKey=HKEY_CURRENT_USER\Environment"
set "regValue=Path"

:: 从注册表读取值
for /f "tokens=2*" %%i in ('reg query %regKey% /v %regValue% ^| findStr "SZ"') do (
    set "regValueData=%%j"
)
echo "%regValueData%"
:: 检查环境变量中是否包含指定的子字符串
echo %regValueData% | findStr %SUBSTRING_TO_FIND% >nul && (
    echo 环境变量中包含 %SUBSTRING_TO_FIND%
) || (
    echo 环境变量中不包含 %SUBSTRING_TO_FIND%
    setx Chrome "%Chrome%" /M
    reg add %regKey% /v %regValue% /f /t REG_EXPAND_SZ /d "%regValueData%;%%%ChromeName%%%"
)

:: 指定要读取的注册表项和值名
set regKey2="HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\Environment"
set "regValue2=Path"

:: 从注册表读取值
for /f "tokens=2*" %%i in ('reg query %regKey2% /v %regValue2% ^| findStr "SZ"') do (
    set "regValueData2=%%j"
)
echo "%regValueData2%"
:: 检查环境变量中是否包含指定的子字符串
echo %regValueData2% | findStr %SUBSTRING_TO_FIND% >nul && (
    echo 环境变量中包含 %SUBSTRING_TO_FIND%
) || (
    echo 环境变量中不包含 %SUBSTRING_TO_FIND%
    setx Chrome "%Chrome%" /M
    reg add %regKey2% /v %regValue2% /f /t REG_EXPAND_SZ /d "%regValueData2%;%%%ChromeName%%%"
)

:End
endlocal
::pause