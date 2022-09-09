################# ! IMPORTANT ! #############
# make sure NEO4J-Graphdatabase is running  #

#import library from neo4j to access database from python
from neo4j import GraphDatabase


#setup uri to access databse
uri = "bolt://localhost:7687"
#setup driver to access Graphdatabase
driver = GraphDatabase.driver(uri, auth=("neo4j", "Masterarbeit"))

#get all data in graphdatabase for given node
def get_nodeData(token):
    with driver.session() as session:
        token_data = session.run("MATCH (n) WHERE n.name = '" + token + "' RETURN n")
        return token_data.data()

#gets alias of given token if it exists in graphdatabase
def get_aliases(token):
    with driver.session() as session:
        alias_data = session.run("MATCH (n)-[]-(a:ALIASES) WHERE n.name = '" + token + "' RETURN n.name AS source, a.name AS target")
        return alias_data.data()

#calculate shortestpath between 2 known nodes
#parameter: depth or length of path from node to node
def get_shortestPathBetween2Nodes(source,target, depth):
    with driver.session() as session:
        shortest_path = session.run("MATCH (s:ITEM {name : '" + source + "'}), (t {name : '" + target + "'}), path = shortestPath((s)-[*.." + depth + "]-(t)) RETURN path")
        return shortest_path.data()

#caluclates shortest path for given source node to any node labeleed with ":clothing"
def get_shortestPathToClothes(source):
    with driver.session() as session:
        shortest_path = session.run("MATCH p=shortestPath((selectedNode {name:'" + source + "'})-[*]-(y:CLOTHING)) RETURN length(p) AS l, collect(y.name) as targets, [n in nodes(p) | n.name] as NodePath, [r in relationships(p) | type(r)] as RelationshipPath ORDER BY l LIMIT 1")
        return shortest_path.data()

#gets shortest path for given node to a node labeled with ":clothing"
#only bert nearest relationships allowed no W2V,GLove,FastText or combined value
def get_shortestPathToClothesOnlyBERT(source):
    with driver.session() as session:
        shortest_path = session.run("MATCH p=shortestPath((selectedNode {name:'" + source + "'})-[*]-(y:CLOTHING)) WHERE NONE (r in relationships(p)  WHERE type(r)='GLOVE' OR type(r)='FASTTEXT' OR type(r)='WORD2VEC' OR type(r)='STATIC_MODELS_COMBINED') RETURN length(p) AS l, collect(y.name) as targets, [n in nodes(p) | n.name] as NodePath, [r in relationships(p) | type(r)] as RelationshipPath ORDER BY l LIMIT 1")
        return shortest_path.data()

#gets shortest path for given node to a node labeled with ":clothing"
#without bert (BMF_IDF) relationships
def get_shortestPathToClothesWithoutBERT(source):
    with driver.session() as session:
        shortest_path = session.run("MATCH p=shortestPath((selectedNode {name:'" + source + "'})-[*]-(y:CLOTHING)) WHERE NONE (r in relationships(p)  WHERE type(r)='BMF_IDF') RETURN length(p) AS l, collect(y.name) as targets, [n in nodes(p) | n.name] as NodePath, [r in relationships(p) | type(r)] as RelationshipPath ORDER BY l LIMIT 1")
        return shortest_path.data()

#get Label fo node in graphdatabse
def get_nodeLabel(token):
    with driver.session() as session:
        node_label = session.run("MATCH (n {name:'"+ token +"'}) RETURN labels(n)")
        return node_label.data()[0]["labels(n)"][0]

#for given node labeled as clothing get all addional details about gender,ageGroup,masterCategory and subCategory
def get_clothingDetails(token):
    with driver.session() as session:
        clothing_details = session.run("MATCH (n {name:'"+ token +"'}) RETURN n.name AS Clothing, n.masterCategory AS Category, n.subCategory AS SubCategory, n.ageGroup_detailed AS AgeGroup, n.gender_detailed AS Gender")
        return clothing_details.data()
    

