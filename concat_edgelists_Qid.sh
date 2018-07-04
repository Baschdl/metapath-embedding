#!/usr/bin/env bash
i=0
while read -r; do
    fname="${REPLY}"
    tail -n +2 $fname | tr , " " | tr -d \" >> all-edgelist-wikidata-Qid.csv
done < <(find . -maxdepth 1 -type f -regextype sed -regex '.*/edgelist-wikidata-[0-9]\+-Qid.csv')