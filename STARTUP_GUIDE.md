# 🏃 项目启动清单

> 开发前按顺序启动以下服务，确保项目正常运行

---

## 1. 基础设施服务（必须）

### 1.1 MySQL

```bash
# Windows服务方式（已设置开机自启，检查是否运行）
# 或手动启动：
net start mysql
```

**验证：** `mysql -u root -p` 能连接

---

### 1.2 Redis

```bash
# 已安装到 D:\DevelopTools\Redis
# 检查服务状态：
net start | findstr Redis

# 如果没运行，手动启动：
net start Redis

# 或重启服务：
net stop Redis
net start Redis
```

**验证：** `redis-cli ping` 返回 `PONG`

---

## 2. 开发工具验证

### 2.1 IDEA启动检查

```
□ MySQL Database 连接正常（绿色勾）
□ Redis Database 连接正常（绿色勾）
□ Maven 依赖已下载（右侧Maven面板无红字）
```

---

## 3. 后端服务 (food-service)

```bash
# 方式1：IDEA中启动
# 找到 FoodServiceApplication.java → 右键 → Run

# 方式2：命令行启动
cd food-visualization/food-service
mvn spring-boot:run

# 方式3：运行jar包
java -jar target/food-service-1.0.0.jar
```

**验证：** 浏览器访问 `http://localhost:8080` 或 `http://localhost:8080/api/xxx`

---

## 4. 前端服务 (food-vue)

```bash
# 进入前端目录
cd food-visualization/food-vue

# 安装依赖（如首次运行）
npm install

# 启动开发服务器
npm run dev
```

**验证：** 浏览器访问 `http://localhost:5173` 或控制台显示的地址

---

## 5. 数据采集（如需更新数据）

```bash
# 激活虚拟环境
cd food-visualization/food-spider
venv\Scripts\activate

# 运行爬虫
scrapy crawl dianping

# 或运行指定脚本
python run_spider.py
```

---

## 6. 服务状态速查

| 服务 | 默认端口 | 检查命令 |
|------|----------|----------|
| MySQL | 3306 | `mysql -u root -p` |
| Redis | 6379 | `redis-cli ping` |
| SpringBoot | 8080 | `curl http://localhost:8080` |
| Vue Dev | 5173 | 浏览器访问 |

---

## ⚠️ 常见问题

### Redis连接失败
```bash
# 检查服务是否运行
net start | findstr Redis

# 重启服务
net stop Redis
net start Redis
```

### MySQL连接失败
```bash
# 检查服务状态
net start | findstr mysql

# 启动MySQL服务
net start mysql
```

### 端口被占用
```bash
# 查看端口占用
netstat -ano | findstr 8080
netstat -ano | findstr 5173

# 结束占用进程（根据PID）
taskkill /PID <PID> /F
```

---

## 🚀 一键启动脚本（可选）

如需更方便，可以创建 `start.bat`：

```batch
@echo off
echo ========================================
echo   项目启动中...
echo ========================================

echo [1/4] 检查 MySQL...
net start | findstr MySQL > nul
if %errorlevel% neq 0 (
    echo MySQL 未运行，正在启动...
    net start MySQL
)

echo [2/4] 检查 Redis...
net start | findstr Redis > nul
if %errorlevel% neq 0 (
    echo Redis 未运行，正在启动...
    net start Redis
)

echo [3/4] 服务检查完成！
echo.
echo 请在 IDEA 中启动：
echo   1. FoodServiceApplication (后端)
echo   2. npm run dev (前端)
echo.
pause
```

---

## 📝 快速笔记

```
日期：___________
今日任务：___________
遇到的问题：___________
解决方法：___________
```

---

*最后更新：2025-05-29*
