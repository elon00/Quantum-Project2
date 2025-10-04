#!/bin/bash

# Quantum Project 2 Deployment Script
# Professional deployment automation for the enhanced Deutsch-Jozsa algorithm

set -euo pipefail

# Configuration
PROJECT_NAME="quantum-project2"
DOCKER_IMAGE="${PROJECT_NAME}:latest"
LOG_FILE="deployment.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# Check requirements
check_requirements() {
    log_info "Checking deployment requirements..."

    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    # Check if git is installed
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed. Please install Git first."
        exit 1
    fi

    log_success "All requirements satisfied"
}

# Build Docker image
build_image() {
    log_info "Building Docker image: $DOCKER_IMAGE"

    if docker build -t "$DOCKER_IMAGE" . >> "$LOG_FILE" 2>&1; then
        log_success "Docker image built successfully"
    else
        log_error "Failed to build Docker image"
        exit 1
    fi
}

# Run tests in container
run_tests() {
    log_info "Running test suite in container..."

    if docker run --rm -v "$(pwd)":/app "$DOCKER_IMAGE" python -m pytest tests/ -v >> "$LOG_FILE" 2>&1; then
        log_success "All tests passed"
    else
        log_error "Some tests failed. Check logs for details."
        exit 1
    fi
}

# Deploy application
deploy_app() {
    log_info "Deploying application..."

    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose down >> "$LOG_FILE" 2>&1 || true

    # Start new containers
    if docker-compose up -d >> "$LOG_FILE" 2>&1; then
        log_success "Application deployed successfully"

        # Wait for health check
        log_info "Waiting for application to be healthy..."
        sleep 10

        # Check container status
        if docker-compose ps | grep -q "Up"; then
            log_success "Application is running and healthy"
        else
            log_warning "Application may not be fully healthy yet"
        fi
    else
        log_error "Failed to deploy application"
        exit 1
    fi
}

# Show deployment status
show_status() {
    log_info "Deployment Status:"
    echo
    echo "Container Status:"
    docker-compose ps
    echo
    echo "Recent Logs:"
    docker-compose logs --tail=10
    echo
    echo "Application URLs:"
    echo "  - Local: http://localhost:8000 (if web interface is implemented)"
    echo "  - API: Available via Docker network"
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."
    rm -f "$LOG_FILE"
}

# Main deployment flow
main() {
    echo "🚀 Quantum Project 2 Professional Deployment"
    echo "============================================="
    echo

    # Create log file
    touch "$LOG_FILE"

    # Trap cleanup on exit
    trap cleanup EXIT

    # Run deployment steps
    check_requirements
    build_image
    run_tests
    deploy_app
    show_status

    echo
    log_success "Deployment completed successfully! 🎉"
    echo
    echo "Next steps:"
    echo "  - View logs: docker-compose logs -f"
    echo "  - Stop app: docker-compose down"
    echo "  - Restart: docker-compose restart"
    echo "  - View status: ./deploy.sh status"
}

# Handle command line arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "status")
        show_status
        ;;
    "test")
        run_tests
        ;;
    "build")
        build_image
        ;;
    "clean")
        log_info "Cleaning up..."
        docker-compose down -v >> "$LOG_FILE" 2>&1 || true
        docker image rm "$DOCKER_IMAGE" >> "$LOG_FILE" 2>&1 || true
        log_success "Cleanup completed"
        ;;
    *)
        echo "Usage: $0 {deploy|status|test|build|clean}"
        echo
        echo "Commands:"
        echo "  deploy  - Full deployment (default)"
        echo "  status  - Show deployment status"
        echo "  test    - Run tests only"
        echo "  build   - Build Docker image only"
        echo "  clean   - Remove containers and images"
        exit 1
        ;;
esac