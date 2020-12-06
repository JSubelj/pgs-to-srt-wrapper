docker stop tmp;
docker rm tmp;
docker build  . -t tmp;
docker run -v /media:/downloads -e SKIP_DISCOVERY=TRUE -e SLEEPING_TIME_S=1 --name tmp tmp;