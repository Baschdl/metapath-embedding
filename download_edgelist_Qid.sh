#!/usr/bin/env bash
number_of_nodes=46000000
size_of_download_in_nodes=100000

i=1

# Rounding up
while [ ${i} -lt  $(( (number_of_nodes+(size_of_download_in_nodes-1) ) / size_of_download_in_nodes )) ]
do
    echo "Calculating edge list for ID(n1) up to " $((i * size_of_download_in_nodes))
    query=$( echo '{"statements":[{"statement":"MATCH (n1:Entity)--(n2:Entity) WHERE ID(n1) > ' \
        $(( (i-1) * size_of_download_in_nodes)) ' AND ID(n1) < ' $((i * size_of_download_in_nodes)) \
        ' RETURN n1.id as n1, n2.id as n2"}]}' )
    curl -H accept:application/json -H content-type:application/json \
         -d "${query}" \
         -u neo4j:caramelBunny1998\
         http://localhost:8888/db/data/transaction/commit \
         | jq -r '(.results[0]) | .columns,.data[].row | @csv' > edgelist-wikidata-$((i * size_of_download_in_nodes)).csv
    i=$((i + 1))
done