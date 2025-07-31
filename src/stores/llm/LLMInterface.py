from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """
    Abstract base class for LLM (Large Language Model) interfaces.
    This class defines the methods that any LLM interface should implement.
    """
    def __init__(self):
        pass

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """
        Set the model to be used for text generation.
        :param model_id: Identifier for the model to be used.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def get_generation_model(self) -> str:
        """
        Get the identifier of the current generation model.
        :return: The model identifier as a string.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_dimensions: int = None):
        """
        Set the model to be used for text embedding.
        :param model_id: Identifier for the embedding model to be used.
        :param embedding_dimensions: Optional dimensions for the embedding model.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def get_embedding_model(self) -> str:
        """
        Get the identifier of the current embedding model.
        :return: The embedding model identifier as a string.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None, temperature: float=None) -> str:
        """
        Generate text based on the provided prompt.
        :param prompt: The input text to generate a response for.
        :param chat_history: Optional chat history to provide context.
        :param max_output_tokens: Maximum number of tokens to generate.
        :param temperature: Sampling temperature for text generation.
        :return: Generated text as a string.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def embed_text(self, text: str, doc_type: str=None) -> list:
        """
        Embed the provided text into a vector representation.
        :param text: The input text to be embedded.
        :param type: The type of embedding to be used 
        :return: A list representing the embedded text.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str) -> dict:
        """
        Construct a prompt based on a template and additional parameters.
        :param prompt: The base prompt text.
        :param role: The role to be included in the prompt (e.g., "user", "assistant").
        :return: The constructed prompt as a dictionary.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")