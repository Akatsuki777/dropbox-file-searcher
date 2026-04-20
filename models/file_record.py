from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class FileRecord:
    name : str
    path : str
    size : int | None = None
    modified_time : datetime | None = None
    extension: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    
