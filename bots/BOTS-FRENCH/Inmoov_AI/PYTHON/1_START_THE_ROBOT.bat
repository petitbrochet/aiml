taskkill.exe /F /IM java.exe
taskkill.exe /F /IM javaW.exe
taskkill.exe /F /IM chrome.exe
del myrobotlab.log
java -jar myrobotlab.jar -invoke python execFile %cd%/INMOOV-AI_startup.py -service GUIService GUIService python Python