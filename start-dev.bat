@echo off
echo Starting React Movies Application...
echo.

echo Starting Flask Backend...
start "Flask Backend" cmd /k "cd backend && python app.py"

timeout /t 3 /nobreak > nul

echo Starting React Frontend...
start "React Frontend" cmd /k "npm run dev"

echo.
echo Both servers are starting...
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
echo.
pause