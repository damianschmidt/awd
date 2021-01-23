ECHO ON

REM clear interface
docker-compose -f docker/docker-compose.yml down --volumes

REM backend
docker-compose -f docker/docker-compose.yml build "backend"
docker-compose -f docker/docker-compose.yml up -d "backend"

REM frontend
docker-compose -f docker/docker-compose.yml build "frontend"
docker-compose -f docker/docker-compose.yml up -d "frontend"

REM follow
docker-compose -f docker/docker-compose.yml logs --follow --tail 50 "backend" &
docker-compose -f docker/docker-compose.yml logs --follow --tail 50 "frontend" &
