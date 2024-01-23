from faker import Faker
from neo4j import GraphDatabase

URI = "neo4j+s://f53af4cc.databases.neo4j.io"
AUTH = ("neo4j", "1Ob6tEcO0946BsXr9ggRQmVe6834TS68qJikhcTUWJM")

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

passport = driver.execute_query(query_='Create (id:IdDocumentTypes {name:"passport"})\nRETURN ID(id) AS id')
id_card = driver.execute_query(query_='Create (id:IdDocumentTypes {name:"id_card"})\nRETURN ID(id) AS id')

def add_and_retrieve_node(tx, label, properties):
    result = tx.run(f"CREATE (node:{label} $properties) RETURN id(node) AS nodeId, node", properties=properties)
    record = result.single()
    return record["nodeId"], record["node"]

# Create a new node with a label and properties
label = "YourLabel"
properties = {"propertyName": "propertyValue"}

with driver.session() as session:
    nodeId, newNode = session.write_transaction(add_and_retrieve_node, label, properties)

    driver.execute_query(query_=f"Match (node)\n Where ID(node) = {nodeId}\n"
                                f"Match (node2)\n Where ID(node2) = {nodeId2}\n"
                                f"Create (node)-[:NODE1_NODE2]->(node2)"
                                f"Create (node2)-[:NODE2_NODE1]->(node)")

# Print the results
print(f"Node ID: {nodeId}")
print("Node:")
print(newNode)
