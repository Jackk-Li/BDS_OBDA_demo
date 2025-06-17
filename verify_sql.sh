#!/bin/bash
# Direct SQL query for comparison

echo "Direct SQL query results (no inference)"
echo "======================================"

echo -e "\n1. Directly query Professors in the employees table:"
mysql -u root -p university_demo -e "
SELECT name FROM employees WHERE position = 'Professor';
"

echo -e "\n2. Try to query 'Person' (this concept does not exist in SQL):"
echo "   SQL cannot understand that Person includes Employee and Student"

echo -e "\n3. Query employees with teaching assignments (requires JOIN):"
mysql -u root -p university_demo -e "
SELECT DISTINCT e.name 
FROM employees e 
JOIN teaching_records t ON e.emp_id = t.emp_id;
"

echo -e "\nCompare with SPARQL query results to see the inference effect"

