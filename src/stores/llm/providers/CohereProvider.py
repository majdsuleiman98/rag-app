from ..LLMInterface import LLMInterface
from ..LLMEnums import CohereEnums, DocumentTypeEnums
import cohere

class CohereProvider(LLMInterface):
    """
    Implementation of the LLMInterface for Cohere's API.
    This class provides methods to interact with Cohere's text generation and embedding models.
    """
    def __init__(self, api_key: str, 
                    default_input_max_characters: int=1000, 
                    default_output_max_tokens: int=1000, 
                    default_temperature: float=0.1):
        
        super().__init__()
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_output_max_tokens = default_output_max_tokens
        self.default_temperature = default_temperature
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_dimensions = None
        self.client = cohere.ClientV2(api_key=self.api_key)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id

    def get_generation_model(self) -> str:
        return self.generation_model_id if self.generation_model_id else "No generation model set."
    
    def set_embedding_model(self, model_id: str, embedding_dimensions: int):
        self.embedding_model_id = model_id
        self.embedding_dimensions = embedding_dimensions
    
    def get_embedding_model(self) -> str:
        return self.embedding_model_id if self.embedding_model_id else "No embedding model set."
    
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None, temperature: float=None) -> str:
        if not self.client:
            raise ValueError("OpenAI client is not initialized.")
        if not self.generation_model_id:
            raise ValueError("Generation model is not set.")
        
        chat_history.append(self.construct_prompt(prompt, CohereEnums.USER.value))
        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens if max_output_tokens else self.default_output_max_tokens,
            temperature=temperature if temperature else self.default_temperature,
        )
        if response and 'message' in response and len(response['message']['content']) > 0 and response['message']['content'][0].text:
            return response['message']['content'][0].text
        else:
            raise ValueError("Failed to generate text. Response: {}".format(response)) 
    
    
    def process_text(self, text: str) -> str:
        return text[:self.default_input_max_characters].strip() if len(text) > self.default_input_max_characters else text

    def construct_prompt(self, prompt: str, role: str) -> dict:
        return {"role":role, "content":self.process_text(prompt)}


    def embed_text(self, text: str, doc_type: str=None) -> list:
        if not self.embedding_model_id:
            raise ValueError("Embedding model is not set.")
        if not self.client:
            raise ValueError("OpenAI client is not initialized.")
        
        response = self.client.embd(
            texts=[text],
            model=self.embedding_model_id,
            input_type= CohereEnums.DOCUMENT.value if doc_type == DocumentTypeEnums.DOCUMENT.value else CohereEnums.QUERY.value,
            embedding_types=["float"],
        )
        if response and 'data' in response and response['data'][0]['embedding']:
            return response['data'][0]['embedding']
        else:
            raise ValueError("Failed to embed text. Response: {}".format(response))