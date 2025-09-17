@echo off
REM Run permissions migration script using direct database method

echo Running permissions migration script...
cd ..
python scripts/migrate_permissions.py --method=db

echo Done!