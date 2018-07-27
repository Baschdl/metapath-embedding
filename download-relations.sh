#!/usr/bin/env bash
number_of_edges=409000000
size_of_download_in_edges=100000

i=1

# Rounding up
while [ ${i} -lt  $(( (number_of_edges+(size_of_download_in_edges-1) ) / size_of_download_in_edges )) ]
do
    echo "Calculating relation list for ID(r) up to " $((i * size_of_download_in_edges))
    query=$( echo '{"statements":[{"statement":"MATCH ()-[r]-() WHERE ID(r) > ' \
        $(( (i-1) * size_of_download_in_edges)) ' AND ID(r) < ' $((i * size_of_download_in_edges)) \
        ' RETURN r.by as r"}]}' )
    curl -H accept:application/json -H content-type:application/json \
         -d "${query}" \
         -u neo4j:caramelBunny1998\
         http://"$1":"$2"/db/data/transaction/commit \
         | jq -r '(.results[0]) | .columns,.data[].row | @csv' > edgelist-wikidata-relations-$((i * size_of_download_in_edges)).csv
    i=$((i + 1))
done