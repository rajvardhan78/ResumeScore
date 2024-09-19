<<<<<<< HEAD
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .validators import validate_file_extension, validate_file_size
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from .utils import read_uploaded_file, extract_resume_info

# Create your views here.
def home(request: HttpRequest):
    return render(request, 'index.html') # Path: resumeScan/parser/templates/index.html

def upload_resume(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('file'):
        file: UploadedFile = request.FILES['file']
        try:
            print("Starting file validation...")
            ext: str = validate_file_extension(file)
            print("File extension validated.")
            validate_file_size(file)
            print("File size validated.")
            
            file.seek(0)
            print("Reading file content...")
            file_content= read_uploaded_file(file, ext)
            print("File content read successfully.")


            print("Extracting resume information...")
            data = extract_resume_info(file_content)
            print("Resume information extracted successfully.")
            print(f"Data: {data}")


            return JsonResponse({
                'success': True,
                'overall_score': data['overall_score'],
                'section_scores': data['section_scores'],
                'improvements': data['improvements']
            })
        except ValidationError as e:
            print(f"Validation error: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            print(f"Internal server error: {str(e)}")
            return JsonResponse({'success': False, 'error': f"Internal server error: {str(e)}"}, status=500)
    print("Invalid request method or no file uploaded.")
    return JsonResponse({'success': False, 'error': "Invalid request"}, status=400)

=======
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .validators import validate_file_extension, validate_file_size
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError
from .utils import read_uploaded_file, extract_resume_info

# Create your views here.
def home(request: HttpRequest):
    return render(request, 'index.html') # Path: resumeScan/parser/templates/index.html

def upload_resume(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('file'):
        file: UploadedFile = request.FILES['file']
        try:
            print("Starting file validation...")
            ext: str = validate_file_extension(file)
            print("File extension validated.")
            validate_file_size(file)
            print("File size validated.")
            
            file.seek(0)
            print("Reading file content...")
            file_content= read_uploaded_file(file, ext)
            print("File content read successfully.")


            print("Extracting resume information...")
            data = extract_resume_info(file_content)
            print("Resume information extracted successfully.")
            print(f"Data: {data}")


            return render(request, 'index.html', {'data': data})
        except ValidationError as e:
            print(f"Validation error: {e}")
            return render(request, 'index.html', {'error_message': str(e)})
        except Exception as e:
            print(f"Internal server error: {str(e)}")
            return render(request, 'index.html', {'error_message': f"Internal server error: {str(e)}"})
    print("Invalid request method or no file uploaded.")
    return render(request, 'index.html', {'error_message': "Invalid request"})

>>>>>>> origin/main
