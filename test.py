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
                                f"Match (node2)\n Where ID(node2) = {nodeId}\n"
                                f"Create (node)-[:NODE1_NODE2]->(node2)"
                                f"Create (node2)-[:NODE2_NODE1]->(node)")

# Print the results
print(f"Node ID: {nodeId}")
print("Node:")
print(newNode)

RecruitmentExemptionDocumentTypesNames = ["disability_certificate", "certificate_of_completion_of_the_first_degree", "certificate_of_completion_of_the_second_degree",
"certificate_of_completion_of_the_third_degree", "Studium Talent"]
for name in []:
    driver.execute_query('CREATE (n:RecruitmentExemptionDocumentTypes {name: {}})'.format(name))


def extract_id(executed_query):
    [result], _, [key] = executed_query
    return result[key]


passport = extract_id(driver.execute_query(query_='Create (id:IdDocumentTypes {name:"passport"})\nRETURN ID(id)'))
id_card = extract_id(driver.execute_query(query_='Create (id:IdDocumentTypes {name:"id_card"})\nRETURN ID(id)'))

def get_relationship_with_attributes(first_id, second_id, relationship_name, relations_attributes):
    """
    Create a relations with given attributes.
    :param first_id: int
    :param second_id: int
    :param relationship_name: str
    :param relations_attributes: str (in pattern {attr1: "attr1", attr2: "attr2"})
    :return: None
    """
    return "\n".join([
        f'Match (node)\n Where ID(node) = {first_id}',
        f'Match (node2)\n Where ID(node2) = {second_id}',
        'Create (node)-[:{} {}]->(node2)'.format(relationship_name, relations_attributes)
    ])

driver.execute_query(query_=get_relationship_with_attributes(passport, id_card, "FUNNY_RELATION", '{number: 5, type: "typer"}'))
driver.execute_query(
        'CREATE (n:Thresholds {year: %s, round_1: %s, round_2: %s, round_3: %s})\nRETURN ID(n)'
            % (1, 2, 3, 4)
    )
print(passport)
print(id_card)
