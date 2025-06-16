#!/bin/bash
# 运行所有示例查询

echo "OBDA推理演示 - 运行所有查询"
echo "======================================"

for query in queries/*.sparql; do
    echo -e "\n\n执行查询: $(basename $query)"
    echo "--------------------------------------"
    cat "$query" | grep "^#" | sed 's/^# //'
    echo "--------------------------------------"
    
    ./lib/ontop-cli-*/ontop query \
        --ontology=ontology/university.ttl \
        --mapping=mappings/university.obda \
        --properties=config/university.properties \
        --query="$query" \
        --outputFormat=csv
    
    echo -e "\n按Enter继续下一个查询..."
    read
done
