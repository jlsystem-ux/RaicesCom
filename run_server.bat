@echo off
cd /d "C:\Users\shich\Documents\RaicesCom\RaicesCom-master\RaicesCom-master"
call venv\Scripts\activate.bat
python manage.py runserver
pause