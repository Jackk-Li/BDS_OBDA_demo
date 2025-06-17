#!/bin/bash
# Start Ontop SPARQL endpoint

echo "Starting Ontop SPARQL endpoint..."
echo "Access URL: http://localhost:8080/sparql"
echo "Press Ctrl+C to stop the service"

./lib/ontop-cli-*/ontop endpoint \
    --ontology=ontology/university.ttl \
    --mapping=mappings/university.obda \
    --properties=config/university.properties \
    --port=8080 \
    --lazy

