@echo off

:: Set script variables
set fromDir="C:\GISData\Scripts\RobocopySpeedTest\CopyFrom"
:: Leave fromFile empty to copy all files in fromDir directory
set fromFile="20210315_CadastralGISData.gdb.zip"
set toDir="\\2108-jxi\c$\GISData\Scripts\RobocopySpeedTest\CopyTo"

:: Set date and time
set start=%time%

set d=%date:~-4,4%%date:~-7,2%%date:~0,2%
set d=%d: =_%
set t=%time:~0,2%%time:~3,2%%time:~6,2%
set t=%t: =0%

set logfile=C:\GISData\Scripts\RobocopySpeedTest\Backup_%d%_%t%.log

echo.
echo.
echo --------------------------
echo  Copying file (started at %date% %time%)
echo --------------------------
REM robocopy "C:\GISData\Scripts\RobocopySpeedTest\CopyFrom" "\\2108-jxi\c$\GISData\Scripts\RobocopySpeedTest\CopyTo" /E /R:5 /W:15 /MT:32 /NP /xf *.lock /LOG:%logfile%
robocopy %fromDir% %toDir% %fromFile% /IS /IT /NP /LOG:%logfile%
REM robocopy "C:\GISData\Scripts\RobocopySpeedTest\CopyFrom" "C:\GISData\Scripts\RobocopySpeedTest\CopyTo" /IS /IT /NP /LOG:%logfile%
echo.
echo ------------------------
echo  Copying file (ended at %date% %time%)
echo ------------------------
echo Logfile at: %logfile%
echo.

set end=%time%
set options="tokens=1-4 delims=:.,"
for /f %options% %%a in ("%start%") do set start_h=%%a&set /a start_m=100%%b %% 100&set /a start_s=100%%c %% 100&set /a start_ms=100%%d %% 100
for /f %options% %%a in ("%end%") do set end_h=%%a&set /a end_m=100%%b %% 100&set /a end_s=100%%c %% 100&set /a end_ms=100%%d %% 100

set /a hours=%end_h%-%start_h%
set /a mins=%end_m%-%start_m%
set /a secs=%end_s%-%start_s%
set /a ms=%end_ms%-%start_ms%
if %ms% lss 0 set /a secs = %secs% - 1 & set /a ms = 100%ms%
if %secs% lss 0 set /a mins = %mins% - 1 & set /a secs = 60%secs%
if %mins% lss 0 set /a hours = %hours% - 1 & set /a mins = 60%mins%
if %hours% lss 0 set /a hours = 24%hours%
if 1%ms% lss 100 set ms=0%ms%

:: Mission accomplished
set /a totalsecs = %hours%*3600 + %mins%*60 + %secs%
echo.>> %logfile%
echo Copy took %hours%:%mins%:%secs%.%ms% (%totalsecs%.%ms%s total)>> %logfile%

PAUSE