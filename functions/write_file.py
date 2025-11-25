import os

def write_file(working_directory,file_path,content):
    
    working_directory_abs = os.path.abspath(working_directory)
    
    os.makedirs(working_directory, exist_ok=True)
    
    full_path = os.path.join(working_directory_abs,file_path)
    full_path = os.path.abspath(full_path)
    
    try:
        parent_directory = os.path.dirname(full_path)
        
        if not full_path.startswith(working_directory_abs):
            return print(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        os.makedirs(parent_directory, exist_ok=True)
        
        with open(full_path,"w") as f:
            f.write(content)
        
        return print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
        
        
    except Exception as e:
         return f"Error: {e}"

