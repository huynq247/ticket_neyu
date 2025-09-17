@echo off
REM Run simplified permissions migration script that directly connects to PostgreSQL

echo Running permissions migration script...
cd ..
python scripts/direct_db_permissions.py

echo Done!
pause