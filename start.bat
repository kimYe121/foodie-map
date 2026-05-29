@echo off
chcp 65001 > nul
echo ========================================
echo   美食可视化项目 - 服务启动器
echo ========================================
echo.

echo [1/4] 检查 MySQL...
net start | findstr /i mysql > nul
if %errorlevel% neq 0 (
    echo     MySQL 未运行，正在启动...
    net start MySQL
) else (
    echo     MySQL 已运行 ✓
)

echo.
echo [2/4] 检查 Redis...
net start | findstr /i Redis > nul
if %errorlevel% neq 0 (
    echo     Redis 未运行，正在启动...
    net start Redis
) else (
    echo     Redis 已运行 ✓
)

echo.
echo [3/4] 检查端口占用...
netstat -ano | findstr ":8080" | findstr LISTENING > nul
if %errorlevel% equ 0 (
    echo     警告：端口 8080 已被占用！
) else (
    echo     端口 8080 可用 ✓
)

echo.
echo ========================================
echo   服务检查完成！
echo ========================================
echo.
echo 下一步：
echo   1. IDEA: 运行 FoodServiceApplication
echo   2. 前端: cd food-vue ^&^& npm run dev
echo.
pause
