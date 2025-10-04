@echo off
REM Quantum Project 2 Windows Deployment Script
REM Professional deployment automation for Windows environments

setlocal enabledelayedexpansion

set "PROJECT_NAME=quantum-project2"
set "DOCKER_IMAGE=%PROJECT_NAME%:latest"
set "LOG_FILE=deployment.log"

REM Colors for output (Windows 10+)
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

if "%1"=="help" goto :show_help
if "%1"=="status" goto :show_status
if "%1"=="test" goto :run_tests
if "%1"=="build" goto :build_image
if "%1"=="clean" goto :cleanup

REM Default action is deploy
goto :deploy

:show_help
echo Usage: deploy.bat [deploy^|status^|test^|build^|clean^|help]
echo.
echo Commands:
echo   deploy  - Full deployment (default)
echo   status  - Show deployment status
echo   test    - Run tests only
echo   build   - Build Docker image only
echo   clean   - Remove containers and images
echo   help    - Show this help message
goto :eof

:log_info
echo [INFO] %~1 >> "%LOG_FILE%"
echo %~1
goto :eof

:log_success
echo [SUCCESS] %~1 >> "%LOG_FILE%"
echo %~1
goto :eof

:log_warning
echo [WARNING] %~1 >> "%LOG_FILE%"
echo %~1
goto :eof

:log_error
echo [ERROR] %~1 >> "%LOG_FILE%"
echo %~1
goto :eof

:check_requirements
call :log_info "Checking deployment requirements..."

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker is not installed. Please install Docker Desktop first."
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1 || docker compose version >nul 2>&1
if errorlevel 1 (
    call :log_error "Docker Compose is not installed. Please install Docker Compose first."
    exit /b 1
)

call :log_success "All requirements satisfied"
goto :eof

:build_image
call :log_info "Building Docker image: %DOCKER_IMAGE%"

docker build -t "%DOCKER_IMAGE%" . >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :log_error "Failed to build Docker image"
    exit /b 1
)

call :log_success "Docker image built successfully"
goto :eof

:run_tests
call :log_info "Running test suite in container..."

docker run --rm -v "%cd%":/app "%DOCKER_IMAGE%" python -m pytest tests/ -v >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :log_error "Some tests failed. Check logs for details."
    exit /b 1
)

call :log_success "All tests passed"
goto :eof

:deploy
echo 🚀 Quantum Project 2 Professional Deployment
echo =============================================
echo.

REM Create log file
type nul > "%LOG_FILE%"

call :check_requirements
call :build_image
call :run_tests

call :log_info "Deploying application..."

REM Stop existing containers
call :log_info "Stopping existing containers..."
docker-compose down >> "%LOG_FILE%" 2>&1

REM Start new containers
docker-compose up -d >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    call :log_error "Failed to deploy application"
    exit /b 1
)

call :log_success "Application deployed successfully"

REM Wait for health check
call :log_info "Waiting for application to be healthy..."
timeout /t 10 /nobreak >nul

call :show_status
goto :eof

:show_status
call :log_info "Deployment Status:"
echo.
echo Container Status:
docker-compose ps
echo.
echo Recent Logs:
docker-compose logs --tail=10
echo.
echo Application URLs:
echo   - Local: http://localhost:8000 (if web interface is implemented)
echo   - API: Available via Docker network
goto :eof

:cleanup
call :log_info "Cleaning up..."
docker-compose down -v >> "%LOG_FILE%" 2>&1
docker image rm "%DOCKER_IMAGE%" >> "%LOG_FILE%" 2>&1
call :log_success "Cleanup completed"
goto :eof