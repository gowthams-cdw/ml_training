from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileVersion:
    version_id: str
    content_id: str
    timestamp: datetime
    size: int
