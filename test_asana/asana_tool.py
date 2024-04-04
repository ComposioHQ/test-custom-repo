from shared.composio_tools.lib import Tool, Action
from pydantic import BaseModel, Field
import requests
from utils.schema import ListModel


# Base request schema for Asana API
class AsanaRequest(BaseModel):
    workspace: str = Field(..., description="Workspace ID")


# ----------------------------------
#         Subtask Actions
# ----------------------------------

class CreateSubtaskRequest(AsanaRequest):
    task_id: str = Field(..., description="Parent Task ID")
    name: str = Field(..., description="Name of the subtask")
    assignee: str = Field(None, description="Assignee ID")
    assignee_status: str = Field(None, description="Assignee status")
    completed: bool = Field(False, description="Whether the subtask is completed")
    due_on: str = Field(None, description="Due date for the subtask")
    liked: bool = Field(False, description="Whether the subtask is liked")
    notes: str = Field(None, description="Subtask notes")


class CreateSubtaskResponse(BaseModel):
    id: str = Field(..., description="ID of the created subtask")


class CreateSubtask(Action):
    """
    Create a subtask under a specific task.
    """
    _display_name = "Create Subtask"
    _request_schema = CreateSubtaskRequest
    _response_schema = CreateSubtaskResponse

    def execute(self, req: _request_schema, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/api/1.0/tasks/{req.task_id}/subtasks"
        headers = authorisation_data["headers"]
        data = {"data": req.dict(exclude_none=True)}  # Exclude fields with None values
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            execution_details = {"executed": True}
            response_data = response.json()["data"]
        else:
            execution_details = {"executed": False}
            response_data = {"error": response.json()}
        return {
            "execution_details": execution_details,
            "response_data": response_data
        }


class GetSubtasksRequest(AsanaRequest):
    task_id: str = Field(..., description="Parent Task ID")
    limit: int = Field(100, description="Max number of results to return")
    return_all: bool = Field(False, description="Whether to return all results")


class GetSubtasksResponseSingleItem(BaseModel):
    id: str = Field(..., description="ID of the subtask")
    name: str = Field(..., description="Name of the subtask")
    # ... Add other relevant fields


class GetSubtasks(Action):
    """
    Get subtasks for a specific task.
    """
    _display_name = "Get Subtasks"
    _request_schema = GetSubtasksRequest
    _response_schema = ListModel[GetSubtasksResponseSingleItem]

    def execute(self, req: _request_schema, authorisation_data: dict):
        url = f"{authorisation_data['base_url']}/api/1.0/tasks/{req.task_id}/subtasks"
        headers = authorisation_data["headers"]
        params = {"limit": req.limit}
        if req.return_all:
            # Implement logic to fetch all subtasks using pagination
            pass
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            execution_details = {"executed": True}
            response_data = {"subtasks": response.json()["data"]}
        else:
            execution_details = {"executed": False}
            response_data = {"error": response.json()}
        return {
            "execution_details": execution_details,
            "response_data": response_data
        }


# ----------------------------------
#         Task Actions
# ----------------------------------

# ... (Implement Task actions like Create Task, Delete Task, etc.)

# ----------------------------------
#         Other Actions
# ----------------------------------

# ... (Implement other actions like Add Task Comment, etc.)


class Asana(Tool):
    """
    Connect to Asana to manage tasks, projects, subtasks, and more.
    """
    def actions(self) -> list:
        return [
            CreateSubtask,
            GetSubtasks,
            # ... Add other implemented actions here
        ]

    def triggers(self) -> list:
        return []
    
__all__ = ["Asana"]