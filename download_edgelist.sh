curl -H accept:application/json -H content-type:application/json \
     -d '{"statements":[{"statement":"MATCH (p1:Entity)--(p2:Entity) WHERE ID(n1) < 100000 RETURN ID(p1) as p1, ID(p2) as p2 LIMIT 10"}]}' \
     -u neo4j:caramelBunny1998\
     http://localhost:8888/db/data/transaction/commit \
     | jq -r '(.results[0]) | .columns,.data[].row | @csv' > edgelist-wikidata-100000.csv