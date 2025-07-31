from enum import Enum

class LLMEnums(Enum):
    OPENAI = "openai"
    COHERE = "cohere"
    QROQ = "qroq"

class OpenAIEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class CohereEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"
    DOCUMENT = "search_document"
    QUERY = "search_query"

class GroqEnums(Enum):
    SYSTEM="system"
    USER="user"

class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"