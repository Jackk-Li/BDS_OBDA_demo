#!/bin/bash
# 运行单个SPARQL查询

if [ $# -eq 0 ]; then
    echo "用法: ./run_query.sh <查询文件>"
    echo "例如: ./run_query.sh queries/01_all_persons.sparql"
    exit 1
fi

echo "执行查询: $1"
echo "============================="

./lib/ontop-cli-*/ontop query \
    --ontology=ontology/university.ttl \
    --mapping=mappings/university.obda \
    --properties=config/university.properties \
    --query="$1" \
    --outputFormat=csv
