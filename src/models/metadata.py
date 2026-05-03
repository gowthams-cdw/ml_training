from datetime import datetime
from dataclasses import dataclass, field

from models.file_version import FileVersion
from models.permissions import Permissions

@dataclass
class FileMetadata:
    file_id: str
    name: str
    content_id: str

    size: int

    created_at: datetime
    modified_at: datetime

    permissions: Permissions

    versions: list[FileVersion] = field(default_factory=list)
