#!/bin/bash

# CodeSage Test Runner
# This script makes it easy to run tests for both backend and frontend

set -e

echo "🧪 CodeSage Test Runner"
echo "========================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is available
if command -v docker &> /dev/null && docker ps &> /dev/null; then
    USE_DOCKER=true
    echo -e "${BLUE}✓ Docker detected - using Docker for backend tests${NC}"
    echo -e "${BLUE}  (Frontend tests run locally - frontend container is production-only)${NC}"
else
    USE_DOCKER=false
    echo -e "${YELLOW}⚠ Docker not available - using local environment${NC}"
fi

echo ""

# Function to run backend tests
run_backend_tests() {
    echo -e "${BLUE}Running Backend Tests...${NC}"
    echo "-------------------"
    
    if [ "$USE_DOCKER" = true ]; then
        docker compose exec backend pytest tests/ -v "$@"
    else
        cd backend
        if [ ! -d "venv" ]; then
            echo -e "${YELLOW}⚠ Virtual environment not found. Creating one...${NC}"
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
        else
            source venv/bin/activate
        fi
        pytest tests/ -v "$@"
        cd ..
    fi
}

# Function to run frontend tests
run_frontend_tests() {
    echo -e "${BLUE}Running Frontend Tests...${NC}"
    echo "-------------------"
    
    # Frontend container is production-only (nginx), so always run tests locally
    # This ensures we have npm/node available for testing
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠ Dependencies not found. Installing...${NC}"
        npm install --legacy-peer-deps
    fi
    npm test
    cd ..
}

# Function to run all tests
run_all_tests() {
    echo -e "${GREEN}Running All Tests${NC}"
    echo "=================="
    echo ""
    
    run_backend_tests
    echo ""
    run_frontend_tests
}

# Parse arguments
case "${1:-all}" in
    backend)
        run_backend_tests "${@:2}"
        ;;
    frontend)
        run_frontend_tests
        ;;
    all)
        run_all_tests
        ;;
    coverage)
        echo -e "${GREEN}Running Tests with Coverage${NC}"
        echo "=========================="
        echo ""
        echo -e "${BLUE}Backend Coverage...${NC}"
        if [ "$USE_DOCKER" = true ]; then
            docker compose exec backend pytest tests/ --cov=app --cov-report=html --cov-report=term
        else
            cd backend
            source venv/bin/activate
            pytest tests/ --cov=app --cov-report=html --cov-report=term
            cd ..
        fi
        echo ""
        echo -e "${BLUE}Frontend Coverage...${NC}"
        # Frontend container is production-only, so run tests locally
        cd frontend
        if [ ! -d "node_modules" ]; then
            echo -e "${YELLOW}⚠ Dependencies not found. Installing...${NC}"
            npm install --legacy-peer-deps
        fi
        npm run test:coverage
        cd ..
        ;;
    help|--help|-h)
        echo "Usage: ./run-tests.sh [backend|frontend|all|coverage] [pytest-options]"
        echo ""
        echo "Options:"
        echo "  backend   - Run only backend tests"
        echo "  frontend  - Run only frontend tests"
        echo "  all       - Run all tests (default)"
        echo "  coverage  - Run tests with coverage reports"
        echo "  help      - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run-tests.sh                    # Run all tests"
        echo "  ./run-tests.sh backend            # Run backend tests only"
        echo "  ./run-tests.sh backend -k test_validate  # Run specific backend tests"
        echo "  ./run-tests.sh coverage           # Run with coverage"
        exit 0
        ;;
    *)
        echo -e "${YELLOW}Unknown option: $1${NC}"
        echo "Run './run-tests.sh help' for usage information"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Tests completed!${NC}"

