#!/bin/bash

# Start services
start() {
    echo "Starting ticket management system services..."
    docker-compose up -d
    echo "Services started successfully!"
    echo "API Gateway: http://localhost:3000"
    echo "User Service: http://localhost:8000"
    echo "Ticket Service: http://localhost:8001"
}

# Stop services
stop() {
    echo "Stopping ticket management system services..."
    docker-compose down
    echo "Services stopped successfully!"
}

# View logs
logs() {
    service=$1
    if [ -z "$service" ]; then
        docker-compose logs -f
    else
        docker-compose logs -f $service
    fi
}

# Show help
help() {
    echo "Usage: ./manage.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start       Start all services"
    echo "  stop        Stop all services"
    echo "  restart     Restart all services"
    echo "  logs        View logs for all services"
    echo "  logs [name] View logs for a specific service (e.g., logs api-gateway)"
    echo "  help        Show this help message"
}

# Process command
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    logs)
        logs $2
        ;;
    *)
        help
        ;;
esac