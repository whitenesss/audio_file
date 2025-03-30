from pydantic import BaseModel

class AudioFileBase(BaseModel):
    file_name: str
    file_path: str

class AudioFileCreate(AudioFileBase):
    message: str
    file_id: int

class AudioFileResponse(AudioFileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True