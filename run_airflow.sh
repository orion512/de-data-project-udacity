# echo -e "AIRFLOW_UID=$(id -u)" > .env

docker-compose up airflow-init
docker-compose up

# docker exec <process id> airflow version 
