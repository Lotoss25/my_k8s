docker ps | grep nginx && echo "nginx запущено" || docker run -d --name nginx nginx:latest
