@echo off
cls

:: Set script variables
set homeDir=C:\GISData\AC-AucklandCouncil\DesktopPerformanceIssues\tests_AC_DesktopPerformanceIssues\RobocopySpeedTest
set fromDir="%homeDir%\CopyFrom"
:: Leave fromFile empty to copy all files in fromDir directory
set fromFile="new-zealand-latest-free.shp_20200722.zip"
::set toDir="C:\GISData\Scripts\RobocopySpeedTest\CopyTo"
set toDir="\\2108-jxi\c$\GISData\Scripts\RobocopySpeedTest\CopyTo"
set batFileName=%~n0
echo File Name: %batFileName%

set python_file="%homeDir%\Robocopy_logToCSV.py"

:: For python 3.x
set pythonpath="C:\GISData\ArcGISPro_PythonClone\env\arcgispro-py3-clone\python.exe"

:: For python 2.7
:: SET pythonpath="C:\Python27\ArcGIS10.8\python.exe"

:: Set date and time
set start=%time%

set d=%date:~-4,4%%date:~-7,2%%date:~0,2%
set d=%d: =_%
set t=%time:~0,2%%time:~3,2%%time:~6,2%
set t=%t: =0%

set logfile=logs\%batFileName%_log_%d%_%t%.log

echo.
echo.
echo --------------------------
echo  Copying file (started at %date% %time%)
echo --------------------------

robocopy %fromDir% %toDir% %fromFile% /IS /IT /NP /NFL /LOG:%logfile%

echo.
echo ------------------------
echo  Copying file (ended at %date% %time%)
echo ------------------------
echo Logfile at: %logfile%
echo.

:: Run RoboCopy Log to CSV python script
%pythonpath% %python_file% %batFileName% %logfile%

:: PAUSE
