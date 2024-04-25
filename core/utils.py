import os
from uuid import uuid4


def unique_file_name(instance, filename):
    """
    Generates a unique filename for the given instance and filename.
    Args:
        instance: The instance of the model.
        filename: The original filename.
    Returns:
        A string representing the unique filename.
    """
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('uploads/', filename)
