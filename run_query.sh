#!/bin/bash
# Run a single SPARQL query

if [ $# -eq 0 ]; then
    echo "Usage: ./run_query.sh <query_file>"
    echo "Example: ./run_query.sh queries/01_all_persons.sparql"
    exit 1
fi

echo "Executing query: $1"
echo "============================="

./lib/ontop-cli-*/ontop query \
    --ontology=ontology/university.ttl \
    --mapping=mappings/university.obda \
    --properties=config/university.properties \
    --query="$1" \
    --outputFormat=csv

