#!/bin/bash
# 启动Ontop SPARQL端点

echo "启动Ontop SPARQL端点..."
echo "访问地址: http://localhost:8080/sparql"
echo "按Ctrl+C停止服务"

./lib/ontop-cli-*/ontop endpoint \
    --ontology=ontology/university.ttl \
    --mapping=mappings/university.obda \
    --properties=config/university.properties \
    --port=8080 \
    --lazy
