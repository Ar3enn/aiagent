import os
def get_files_info(working_directory,directory="."):
    
    working_directory_abs = os.path.abspath(working_directory)
    full_dir = os.path.join(working_directory_abs,directory)
    full_dir = os.path.abspath(full_dir)
    
    try:
        
        if not full_dir.startswith(working_directory_abs):
            return print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        elif not os.path.isdir(full_dir):
            return print(f'Error: "{directory}" is not a directory')
    
        for item in os.listdir(full_dir):
            item_name = item
            item = os.path.join(full_dir,item)
            print(f"- {item_name}: file_size:{os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}")
            
    except Exception as e:
        return f"Error: {e}"



   
    
