import os
import subprocess
from google.genai import types

def run_python_file(working_directory,file_path, args=[]):
    
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.join(working_directory_abs,file_path)
    full_path = os.path.abspath(full_path)
    
    try:
        
        if not full_path.startswith(working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(full_path):
            return f'Error: File "{file_path}" not found.'
        
        if  not full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        command_list = ["python", full_path] + args
        completed_process = subprocess.run(args=command_list,timeout=30,cwd=working_directory_abs,capture_output=True,text=True)
        
        output = completed_process.stdout
        if completed_process.stderr:
            output += f"\nSTDERR: {completed_process.stderr}"

        if completed_process.returncode != 0:
            return f"Process exited with code {completed_process.returncode}\n{output}"
        
        if not output.strip():
            return "No Output produced"
            
        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
           
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python script",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)   
