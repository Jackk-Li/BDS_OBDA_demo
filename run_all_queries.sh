#!/bin/bash
# Run all example queries

echo "OBDA Inference Demo - Run All Queries"
echo "======================================"

for query in queries/*.sparql; do
    echo -e "\n\nExecuting query: $(basename $query)"
    echo "--------------------------------------"
    # Display comments from the query file
    cat "$query" | grep "^#" | sed 's/^# //'
    echo "--------------------------------------"
    
    ./lib/ontop-cli-*/ontop query \
        --ontology=ontology/university.ttl \
        --mapping=mappings/university.obda \
        --properties=config/university.properties \
        --query="$query" \
        --outputFormat=csv
    
    echo -e "\nPress Enter to continue to the next query..."
    read
done

