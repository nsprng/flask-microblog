# flask-microblog
Flask Mega-Tutorial series from Miguel Grinberg

## Running in Docker containers

### Create Docker network:
```bash
docker network create microblog
```
### Start MySQL:
```bash
docker run -dit --network microblog --name microblog-db -h db-server -p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=<MYSQL_ROOT_PASSWORD> -e MYSQL_DATABASE="microblog" \
	-e MYSQL_USER="microblog" -e MYSQL_PASSWORD=<MYSQL_MICROBLOG_PASSWORD> \
	mysql/mysql-server:5.7
```
### Start Redis:
```bash
docker run -dit --network microblog --name microblog-redis -h redis-server -p 6379:6379 \ 
        redis:latest
```
### Start Elasticsearch (optional):
```bash
docker run -dit --network microblog --name microblog-elasticsearch -h es-server \
	-p 9200:9200 -p 9300:9300 \
	-e "discovery.type=single-node" \
	elasticsearch:6.8.2
```
### Build an image:
```bash
docker build -t microblog:latest .
```
### Start RQ Worker:
```bash
docker run -dit --network microblog --name microblog-rq-worker -h rq-worker \
	-e SECRET_KEY=<SECRET_KEY> -e MAIL_SERVER=<MAIL_SERVER> -e MAIL_PORT=587 \
	-e MAIL_USE_TLS="true" -e MAIL_USERNAME=<MAIL_USERNAME> -e MAIL_PASSWORD=<MAIL_PASSWORD> \
	-e DATABASE_URL="mysql+pymysql://microblog:<MYSQL_MICROBLOG_PASSWORD>@db-server/microblog" \
	-e REDIS_URL="redis://redis-server:6379/0" \
	-e ELASTICSEARCH_URL="http://es-server:9200" \
	--entrypoint venv/bin/rq \
	microblog:latest \
	worker -u redis://redis-server:6379/0 microblog-tasks
```
### Start Microblog:
```bash
docker run -dit --network microblog --name microblog-app -h app-server -p 5000:5000 \
	-e SECRET_KEY=<SECRET_KEY> -e MAIL_SERVER=<MAIL_SERVER> -e MAIL_PORT=587 \
	-e MAIL_USE_TLS="true" -e MAIL_USERNAME=<MAIL_USERNAME> -e MAIL_PASSWORD=<MAIL_PASSWORD> \
	-e DATABASE_URL="mysql+pymysql://microblog:<MYSQL_MICROBLOG_PASSWORD>@db-server/microblog" \
	-e REDIS_URL="redis://redis-server:6379/0" \
	-e ELASTICSEARCH_URL="http://es-server:9200" \
	microblog:latest
```
### Start Nginx:
```bash
docker run -dit --network microblog --name microblog-nginx -h app-proxy -p 80:80 -p 443:443 \ 
        -v deployment/nginx/default.conf:/etc/nginx/conf.d/default.conf \ 
        nginx:latest
```
### Change MySQL encoding:
```sql
mysql> use microblog
mysql> ALTER DATABASE microblog CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
mysql> ALTER TABLE user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE post CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE notification CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE task CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
