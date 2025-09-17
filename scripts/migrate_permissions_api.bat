@echo off
REM Run permissions migration script using API method

echo Running permissions migration script...
cd ..
python scripts/migrate_permissions.py --method=api

echo Done!