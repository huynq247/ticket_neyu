@echo off
REM Create ticket_db database and migrate permissions

echo Running database creation and permissions migration script...
cd ..
python scripts/create_db_and_permissions.py

echo Done!
pause