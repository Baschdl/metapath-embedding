# Own algorithm

## Build meta-path mining algorithm
- Checkout `mps-between-instances-per_startnode` from https://github.com/KDD-OpenSource/neo4j-graph-algorithms
- `cd neo4j-graph-algorithms && mvn clean install`
- Copy `graph-....jar` to plugins folder

## Import data into neo4j
Import two different wikidata dumps into neo4j instances using https://github.com/findie/wikidata-neo4j-importer

- Mount built neo4j-graph-algorithms plugin
- Allow execution of plugin

## Map wikidata class hierarchy into nodes
- Checkout `multiTypesConversion` from https://github.com/KDD-OpenSource/neo4j-graph-algorithms
- Run hierarchy algorithm
- Run algorithm to copy types from classes to instances

## Clean data
- Remove test label
- Delete all nodes with types != Entity

## Mine meta-paths on t_1 and t_2
- Mount /tmp/between_instances from docker container into local file system
- Optional: Load graph
- Run mining algorithm
- **TODO:** Build training examples with converted meta-paths
- Convert files with `python3 transform_texts.py`
- Concatenate converted meta-path files `echo data/*_converted.txt | xargs cat > data/all.txt`

## Train embeddings on t_1
- Install fastText with `git clone https://github.com/facebookresearch/fastText.git && cd fastText && make`
- Run fastText with `./fasttext skipgram -input data.txt -output model`

## Find new edges in t_2 compared to t_1
- Download the edge lists with `download_edgelist_Qid.sh`
- **TODO:** Add bolder warning for failed downloads
- Append the edge lists to one big list with `concat_edgelists_Qid.sh`
- Find new edges with `python3 find_new_edges.py`

## Mine meta-paths for positive and negative edges
### Positive edges
- Convert list with new edges from previous step to list of neo4j ids with `python3 convert_new_edges_to_neo4j_ids.py --new_edges_list ~/new_edges_t1_t3_undirected.txt --converted_new_edges_list new_edges_t1_t3_undirected_neo4j.txt --user user --password password --uri bolt://localhost:7687`.
Takes around 1,5h.
- Start mining with something like `CALL algo.computeAllMetaPathsBetweenInstances(5, 0, 0.999, {'edgelistFilepath':'/tmp/between_instances/positive_edgelist.txt'})`

### Negative edges
- **TODO:** Sample negative edges in t_1 by looping through mined meta-paths and look which nodes don't have a edge
- **TODO:** Check that they are not in the list of new edges

## Train link prediction classifier
- Labels are the nodes with a new edge, features are the combined embeddings of the meta-paths between the two nodes

# Competitors

## Export edge lists
- Download the edge lists with `download_edgelist.sh`
- **TODO:** Add bolder warning for failed downloads
- Append the edge lists to one big list with `concat_edgelists.sh`
- If neccessary, subsample the nodelist with `shuf -n number_of_nodes all-edgelist.csv > all-edgelist-subsample.csv`

## Convert edge list to bcsr
- **TODO:** Add header line to big edge list
- Install `verse` with `https://github.com/xgfs/verse.git && cd src && make;`
- Convert list to bcsr with `convert-bcsr --format edgelist [--undirected / --directed] /path/to/edgelist /path/to/bcsr`

## Train node embeddings with competitors
- Verse: `verse -input data/karate.bcsr -output karate.bin -dim 128 -alpha 0.85 -threads 4 -nsamples 3`
- DeepWalk: `git clone https://github.com/xgfs/deepwalk-c.git && cd src && make; && [./]deepwalk [...]`
- node2vec: `git clone https://github.com/xgfs/node2vec-c.git && make && [./]node2vec [...]`

## Train link prediction classifier
- Build negative samples
- Labels are the nodes with a new edge, features are the embedding of the two nodes
