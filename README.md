# flask-microblog
Flask Mega-Tutorial series from Miguel Grinberg

## Running in a Docker containers

### Start MySQL:
```bash
docker run -dit --name microblog-db -h db-server -p 3306:3306 \
	-e MYSQL_ROOT_PASSWORD=<MYSQL_ROOT_PASSWORD> -e MYSQL_DATABASE="microblog" \
	-e MYSQL_USER="microblog" -e MYSQL_PASSWORD=<MYSQL_MICROBLOG_PASSWORD> \
	mysql/mysql-server:5.7
```
Change MySQL encoding:
```sql
mysql> use microblog
mysql> ALTER DATABASE microblog CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;
mysql> ALTER TABLE user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE post CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE message CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE notification CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
mysql> ALTER TABLE task CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
### Start Redis:
```bash
docker run -dit --name microblog-redis -h redis-server -p 6379:6379 redis:latest
```
### Start Elasticsearch (optional):
```bash
docker run -dit --name microblog-elasticsearch -h es-server \
	-p 9200:9200 -p 9300:9300 \
	-e "discovery.type=single-node" \
	elasticsearch:6.8.2
```
### Start RQ Worker:
```bash
docker run -dit --name microblog-rq-worker -h rq-worker \
	--link microblog-db:db-server \
	--link microblog-redis:redis-server \
	--link microblog-elasticsearch:es-server \
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
docker run -dit --name microblog-app -h app-server -p 8000:5000 \
	--link microblog-db:db-server \
	--link microblog-redis:redis-server \
	--link microblog-elasticsearch:es-server \
	-e SECRET_KEY=<SECRET_KEY> -e MAIL_SERVER=<MAIL_SERVER> -e MAIL_PORT=587 \
	-e MAIL_USE_TLS="true" -e MAIL_USERNAME=<MAIL_USERNAME> -e MAIL_PASSWORD=<MAIL_PASSWORD> \
	-e DATABASE_URL="mysql+pymysql://microblog:<MYSQL_MICROBLOG_PASSWORD>@db-server/microblog" \
	-e REDIS_URL="redis://redis-server:6379/0" \
	-e ELASTICSEARCH_URL="http://es-server:9200" \
	microblog:latest
```
