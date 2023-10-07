import weaviate

from ace.types import Memory


# The structure of the objects we want to store in weaviate
data_class_definition = {
    "class": "Memory",
    "properties": [
        {
            "dataType": ["date"],
            "name": "time_utc",
        },
        {
            "dataType": ["text"],
            "name": "content"
        }
    ]
}

# This is the weaviate equivalent of table name RDB or collection name in MongoDB
data_class_name = data_class_definition["class"]


class WeaviateMemoryManager:
    def __init__(self, weaviate_url, openai_api_key):
        self.client = weaviate.Client(
            url=weaviate_url,
            additional_headers={
                "X-OpenAI-Api-Key": openai_api_key,
            }
        )
        self.create_weaviate_class_if_doesnt_already_exist(data_class_definition)

    def save_memory(self, memory: Memory):
        self.client.data_object.create(
            memory,
            data_class_name
        )

    def find_relevant_memories(self, search_text, limit) -> list[Memory]:
        """
            Ordered by relevance
        """
        result = (
            self.client.query
            .get("Memory", ["time_utc", "content"])
            .with_near_text({
                "concepts": search_text
            })
            .with_limit(limit)
            # .with_additional(["distance"])
            .do()
        )
        print("find_relevant_memories response: " + str(result))
        return result["data"]["Get"][data_class_name]

    def create_weaviate_class_if_doesnt_already_exist(self, class_definition):
        existing_classes = self.client.schema.get()
        if not any(class_info['class'] == data_class_name for class_info in existing_classes['classes']):
            self.client.schema.create_class(class_definition)
            print(f"Weaviate schema {data_class_name} created successfully")



