import os
import subprocess

def run_python_file(working_directory,file_path, args=[]):
    
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory_abs,file_path)
    full_path = os.path.abspath(full_path)
    
    try:
        
        if not full_path.startswith(working_directory_abs):
            return print(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        
        if not os.path.isfile(full_path):
            return print(f'Error: File "{file_path}" not found.')
        
        if  not full_path.endswith(".py"):
            return print(f'Error: "{file_path}" is not a Python file.')
        
        command_list = ["python", full_path] + args
        completed_process = subprocess.run(args=command_list,timeout=30,cwd=working_directory_abs,capture_output=True,text=True)
        
        if completed_process.returncode != 0:
            return print(f"Process exited with code {completed_process.returncode}")
        if completed_process.stdout == "":
            return print(f"No Output produced")
        
        return print(f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}")
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
           
        
