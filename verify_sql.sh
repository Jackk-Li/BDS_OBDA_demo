#!/bin/bash
# 直接SQL查询用于对比

echo "直接SQL查询结果（无推理）"
echo "======================================"

echo -e "\n1. 直接查询employees表中的Professor："
mysql -u root -p university_demo -e "
SELECT name FROM employees WHERE position = 'Professor';
"

echo -e "\n2. 尝试查询'Person'（SQL中不存在此概念）："
echo "   SQL无法理解Person包含Employee和Student"

echo -e "\n3. 查询有教学任务的员工（需要JOIN）："
mysql -u root -p university_demo -e "
SELECT DISTINCT e.name 
FROM employees e 
JOIN teaching_records t ON e.emp_id = t.emp_id;
"

echo -e "\n对比SPARQL查询结果查看推理效果"
