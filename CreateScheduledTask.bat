@ECHO OFF
CLS

:: Set variables
SET taskschdName=Robocopy\RobocopySpeedTest
SET pythonFilePath=C:\GISData\AC-AucklandCouncil\RobocopySpeedTest\Robocopy_logToCSV.py
SET targetDirList=H:\Documents\Robocopy;U:\CityWide\Transfer\Geospatial\Robocopy
SET pythonProgramPath=C:\GISData\ArcGISPro_PythonCloneArcGISPro_PythonClone\env\arcgispro-py3-clone\python.exe
:: #########################################

ECHO Creating scheduled task...

SCHTASKS /CREATE /SC DAILY /DU 24:00 /RI 60 /TN "%taskschdName%" /TR "'%pythonProgramPath%' '%pythonFilePath%' '%targetDirList%'" /ST 08:00

ECHO Finished creating scheduled task
ECHO.
