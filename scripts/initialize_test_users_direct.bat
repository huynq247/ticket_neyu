@echo off
echo Initializing test users directly in the database...
cd /d D:\NeyuProject\services\user-service
D:\NeyuProject\venv_py310\Scripts\python.exe create_test_users_direct.py
echo Test users initialization complete!
pause