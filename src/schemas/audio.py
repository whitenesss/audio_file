from pydantic import BaseModel

class AudioFileBase(BaseModel):
    message: str
    file_id: int
    file_name: str
    file_path: str

class AudioFileCreate(AudioFileBase):
    pass

class AudioFileResponse(BaseModel):
    id: int
    user_id: int
    file_name: str
    file_path: str

    class Config:
        from_attributes = True