<<<<<<< HEAD
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
import os

VALID_EXTENSIONS=['.pdf', '.docx', '.doc']

def validate_file_extension(file_object: UploadedFile):
    ext: str = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(f"Unsupported file format: {ext}")
    return ext

def validate_file_size(file_object: UploadedFile):
    MAX_SIZE = 2_096_152    # 2MB
    if file_object.size > MAX_SIZE:
=======
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
import os

VALID_EXTENSIONS=['.pdf', '.docx', '.doc']

def validate_file_extension(file_object: UploadedFile):
    ext: str = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(f"Unsupported file format: {ext}")
    return ext

def validate_file_size(file_object: UploadedFile):
    MAX_SIZE = 2_096_152    # 2MB
    if file_object.size > MAX_SIZE:
>>>>>>> origin/main
        raise ValidationError("File is too large! Max size is 2MB.")