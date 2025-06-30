import openai

class AzureOpenAIEmbeddingFunction:
    def __init__(self, api_key, endpoint, deployment_name):
        self.api_key = api_key
        self.endpoint = endpoint
        self.deployment_name = deployment_name
        self.client = openai.AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-12-01-preview",
            azure_endpoint=self.endpoint
        )

    def __call__(self, input):
        # input: list of strings
        response = self.client.embeddings.create(
            input=input,
            model=self.deployment_name
        )
        return [record.embedding for record in response.data] 