from pydantic import BaseModel, ValidationError
import json
import os
import stat

class CommandDescription(BaseModel):
    # Shell command to run
    shell_command: str
    # Name to display in the UI
    name: str
    # Text to display in the UI in details
    description: str

    unique_id: str

    is_executing: bool = False

    def execute(self):
        """
        Execute the shell command.
        """
        print(f"Executing command: {self.shell_command}")
        self.is_executing = True
        try:
            os.system(self.shell_command)
        finally:
            self.is_executing = False


def get_command_list(command_dir: str) -> list[CommandDescription]:
    commands: list[CommandDescription] = []
    for filename in os.listdir(command_dir):
        filepath = os.path.join(command_dir, filename)
        if filename.endswith(".json"):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                    command = CommandDescription(**data, unique_id=f"{filepath}")
                    commands.append(command)
            except (FileNotFoundError, json.JSONDecodeError, ValidationError) as e:
                print(f"Error loading JSON file {filename}: {e}")
        elif os.path.isfile(filepath) and os.access(filepath, os.X_OK):
            command = CommandDescription(
                shell_command=filepath,
                name=filename,
                description=f"Executable file: {filename}",
                unique_id=filepath,
            )
            commands.append(command)
    return commands
