import os
from functions.config import MAX_CHARS
from google.genai import types
def get_file_content(working_directory,file_path):
    
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory_abs,file_path)
    full_path = os.path.abspath(full_path)
    
    try:
        
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(full_path) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
    
        with open(full_path, "r") as f: 
            contents = f.read(MAX_CHARS)
            
        
        if os.path.getsize(full_path) > MAX_CHARS:
            contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            
        return contents   
            
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of a specific file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)    
    
    
   
        
   