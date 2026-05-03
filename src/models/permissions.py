from dataclasses import dataclass

@dataclass
class Permissions:
    read: bool = True
    write: bool = True
    delete: bool = True
