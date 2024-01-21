from pydantic import BaseModel, Field
from api.base.base_schemas import BaseResponse, PaginationParams

# POST /notes
class CreateNoteRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=6, max_length=500)

class CreateNoteResponse(BaseResponse):
    data: dict | None

# GET Pagination /notes
class ReadAllNoteParamRequest(PaginationParams):
    include_deleted: bool = False

class ReadAllNoteResponse(BaseResponse):
    data: dict | None

# GET One Notes /notes/{id}
class ReadNoteResponse(BaseResponse):
    data: dict | None

# PUT /notes/{id}
class UpdateNoteRequest(BaseModel):
    new_title: str = Field(min_length=1, max_length=100)
    new_content: str = Field(min_length=6, max_length=500)

class UpdateNoteResponse(BaseResponse):
    data: dict | None

# DELETE /notes/{id}
class DeleteNoteResponse(BaseResponse):
    data: dict | None
