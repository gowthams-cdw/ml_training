from dataclasses import dataclass, field


@dataclass
class DirectoryNode:
    id: str
    name: str

    parent: "DirectoryNode | None"

    subdirectories: dict[str, "DirectoryNode"] = field(default_factory=dict)

    files: dict[str, str] = field(default_factory=dict)
