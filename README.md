# 📝 Multi-Tier Todo App (Flask + MySQL)

This project is a simple multi-tier Todo application built with:
- **Flask** (Python backend)
- **MySQL 5.7** (Database)

We run the entire stack using **Docker** only (no `docker-compose` required).

---

## 🚀 Steps to Run

### 1. Build the Flask App Docker Image
```bash
docker build -t multtiertodoapp:latest .
```

### 2. Create a Docker Network
```bash
docker network create twotiertodoapp_network
```
### 3. Create a MySQL Volume
```bash
docker volume create twotiertodoapp_data
```
### 4. Run MySQL 5.7
```bash
docker run -d \
  -v twotiertodoapp_data:/var/lib/mysql \
  --network twotiertodoapp_network \
  -e MYSQL_ROOT_PASSWORD=test@123 \
  --name twotiertodoapp_mysql \
  mysql:5.7
```
### 5. Run Flask App
```bash
docker run -d \
  -p 5000:5000 \
  --network twotiertodoapp_network \
  -e DB_SERVER=twotiertodoapp_mysql \
  -e DB_USER=root \
  -e DB_PASSWORD=test@123 \
  -e DB_NAME=todo_db \
  --name twotierapp_flask \
  multtiertodoapp:latest
```
