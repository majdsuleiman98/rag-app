from enum import Enum

class ResponseSignal(Enum):
    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_VALIDATION_FAILURE = "File validation failed."
    FILE_VALIDATION_TYPE_ERROR = "File type is not allowed."
    FILE_VALIDATION_SIZE_ERROR = "File size exceeds the maximum limit."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    FILE_PROCESSING_SUCCESS = "File processing completed successfully."
    FILE_PROCESSONG_FAILURE = "File processing failed."