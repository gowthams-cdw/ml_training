import json
from collections import OrderedDict, defaultdict
from datetime import datetime
from typing import List, Set

from core.exceptions import DuplicateFileError, FileSystemError
from indexing.search_index import SearchIndex
from models.directory import DirectoryNode
from models.file_version import FileVersion
from models.metadata import FileMetadata
from models.permissions import Permissions
from storage.cache import LRUCache
from storage.content_store import ContentStore
from storage.metadata_store import MetadataStore
from storage.persistance import deserialize_directory, serialize_directory
from utils.helpers import current_time, generate_id
from utils.paths import resolve_path, split_path


class FileSystem:
    """
    In-memory file system implementation
    It supports directories, files, metadata management, content storage, caching, and search indexing.
    """

    def __init__(self) -> None:
        self.root = DirectoryNode(id=generate_id(), name="/", parent=None)

        self.metadata_store = MetadataStore()
        self.content_store = ContentStore()
        self.cache = LRUCache(capacity=10)
        self.search_index = SearchIndex()

    def create_directory(self, path: str) -> None:
        """
        creates a directory at the specified path.
        If any intermediate directories do not exist, they will be created as well.
        Args:
            path: the path of the directory to create
        """
        current = self.root

        parts = split_path(path)

        for part in parts:
            if part not in current.subdirectories:
                directory = DirectoryNode(id=generate_id(), name=part, parent=current)
                current.subdirectories[part] = directory

            current = current.subdirectories[part]

    def add_file(self, path: str, content: str):
        """
        creates a file at the specified path with the given content.
        Args:
            path: the path of the file to create
            content: the content of the file to create

        Raises:
            DuplicateFileError: if a file with the same name already exists in the target directory
        """
        parts = split_path(path)

        directory_parts = parts[:-1]
        file_name = parts[-1]

        directory_path = "/" + "/".join(directory_parts)
        directory = resolve_path(self.root, directory_path)

        if file_name in directory.files:
            raise DuplicateFileError(f"File {file_name} already exists.")

        file_id = generate_id()
        content_id = generate_id()
        time = current_time()

        self.content_store.write_content(content_id, content)

        metadata = FileMetadata(
            file_id=file_id,
            name=file_name,
            content_id=content_id,
            size=len(content.encode()),
            created_at=time,
            modified_at=time,
            permissions=Permissions(),
        )

        self.metadata_store.add_metadata(metadata)

        directory.files[file_name] = file_id

        self.search_index.index_file(file_id, content)

    def read_file(self, path: str) -> str:
        """
        computes the content of the file at the specified path and returns it.
        Args:
            path: the path of the file to read

        Returns: the content of the file at the specified path

        Raises:
            FileNotFoundError: if the file does not exist at the specified path
            PermissionError: if the file exists but does not have read permissions
        """
        parts = split_path(path)

        directory_parts = parts[:-1]
        directory_path = "/" + "/".join(directory_parts)

        file_name = parts[-1]

        directory = resolve_path(self.root, directory_path)

        if file_name not in directory.files:
            raise FileNotFoundError(f"File {file_name} not found.")

        file_id = directory.files[file_name]
        metadata = self.metadata_store.get_metadata(file_id)

        if not metadata.permissions.read:
            raise PermissionError("Read permission denied.")

        content_id = metadata.content_id

        cached_content = self.cache.get(content_id)
        if cached_content is not None:
            return cached_content

        content = self.content_store.read_content(content_id)

        self.cache.put(content_id, content)

        return content

    def list_directory(self, path: str) -> list[str]:
        """
        lists the contents of the directory at the specified path.
        Args:
            path: the path of the directory to list

        Returns: a list of the names of the files and subdirectories in the directory at the specified path

        """
        directory = resolve_path(self.root, path)

        subdirectories = list(directory.subdirectories.keys())
        files = list(directory.files.keys())

        return subdirectories + files

    def delete_file(self, path: str) -> None:
        """
        deletes the file at the specified path.

        Args:
            path: the path of the file to delete

        Raises:
            FileSystemError: if the specified path is the root directory or if the file does not exist at the specified path
            FileNotFoundError: if the file does not exist at the specified path
            PermissionError: if the file exists but does not have delete permissions
        """
        if path == "/":
            raise FileSystemError("Cannot delete root directory.")

        parts = split_path(path)

        directory_parts = parts[:-1]
        directory_path = "/" + "/".join(directory_parts)

        file_name = parts[-1]

        directory = resolve_path(self.root, directory_path)

        if file_name not in directory.files:
            raise FileNotFoundError(f"file {file_name} not found.")

        file_id = directory.files[file_name]

        metadata = self.metadata_store.get_metadata(file_id)
        if not metadata.permissions.delete:
            raise PermissionError("Delete permission denied.")

        content_id = metadata.content_id

        self.content_store.delete_content(content_id)
        self.metadata_store.del_metadata(file_id)
        self.cache.remove(content_id)
        self.search_index.remove(file_id)

        del directory.files[file_name]

    def delete_directory(self, path: str):
        """
        deletes the directory at the specified path and all of its contents (files and subdirectories).

        Args:
            path: the path of the directory to delete

        Raises:
            FileSystemError: if the specified path is the root directory or if the directory does not exist at the specified path
        """
        if path == "/":
            raise FileSystemError("Cannot delete root directory.")

        target_directory = resolve_path(self.root, path)

        self._recursive_delete(target_directory)

    def _recursive_delete(self, directory: DirectoryNode):
        """
        utility function that recursively deletes a directory and all of its contents (files and subdirectories).

        Args:
            directory: the directory node to delete
        """
        for child_name in list(directory.subdirectories.keys()):
            child = directory.subdirectories[child_name]
            self._recursive_delete(child)

        for file_name in list(directory.files.keys()):
            file_path = f"{self._build_directory_path(directory)}/{file_name}"
            self.delete_file(file_path)

        if directory.parent:
            del directory.parent.subdirectories[directory.name]

    def _build_directory_path(self, directory: DirectoryNode) -> str:
        """
        utility function that builds the full path of a directory node by traversing up the directory tree.

        Args:
            directory: directory node to build the path for

        Returns: the full path of the directory node

        """
        parts = []

        current = directory

        while current.parent:
            parts.append(current.name)
            current = current.parent

        return "/".join(reversed(parts))

    def move(self, src_file_path: str, dest_file_path: str) -> None:
        """
        moves a file from the source path to the destination path.

        Args:
            dest_file_path: the path to move the file to
            src_file_path: the path to move the file from

        Raises:
            FileNotFoundError: if the file does not exist at the source path or if the destination directory does not exist
            DuplicateFileError: if a file with the same name already exists in the destination directory
        """
        src_parts = split_path(src_file_path)

        src_directory_parts = src_parts[:-1]
        src_directory_path = "/" + "/".join(src_directory_parts)
        src_directory = resolve_path(self.root, src_directory_path)

        src_file_name = src_parts[-1]

        if src_file_name not in src_directory.files:
            raise FileNotFoundError(f"File {src_file_name} not found in source.")

        file_id = src_directory.files[src_file_name]

        deet_parts = split_path(dest_file_path)

        dest_directory_parts = deet_parts[:-1]
        dest_directory_path = "/" + "/".join(dest_directory_parts)
        dest_directory = resolve_path(self.root, dest_directory_path)

        dest_file_name = deet_parts[-1]

        if dest_file_name in dest_directory.files:
            raise DuplicateFileError(
                f"File {dest_file_name} already exists in destination."
            )

        dest_directory.files[dest_file_name] = file_id

        metadata = self.metadata_store.get_metadata(file_id)
        metadata.name = dest_file_name

        del src_directory.files[src_file_name]

    def update_content(self, path: str, new_content: str) -> None:
        """
        updates the content of the file at the specified path with the new content.

        Args:
            path: the path of the file to update
            new_content: the new content to write to the file

        Raises:
            FileNotFoundError: if the file does not exist at the specified path
            PermissionError: if the file exists but does not have write permissions
        """
        parts = split_path(path)

        directory_parts = parts[:-1]
        directory_path = "/" + "/".join(directory_parts)
        directory = resolve_path(self.root, directory_path)

        file_name = parts[-1]

        if file_name not in directory.files:
            raise FileNotFoundError(f"File {file_name} not found.")

        file_id = directory.files[file_name]
        metadata = self.metadata_store.get_metadata(file_id)

        if not metadata.permissions.write:
            raise PermissionError("Write permission denied.")

        time = current_time()

        old_version = FileVersion(
            version_id=generate_id(),
            content_id=metadata.content_id,
            timestamp=time,
            size=metadata.size,
        )

        metadata.versions.append(old_version)
        metadata.size = len(new_content.encode())
        metadata.modified_at = time

        new_content_id = generate_id()
        self.content_store.write_content(new_content_id, new_content)
        metadata.content_id = new_content_id

        self.search_index.remove(file_id)
        self.search_index.index_file(file_id, new_content)

    def read_file_version(self, path: str, version_index: int) -> str:
        """
        reads the content of a specific version of the file at the specified path.

        Args:
            path: the path of the file to read
            version_index: the index of the version to read (0-based index, where 0 is the most recent version)

        Returns: the content of the specified version of the file at the specified path

        Raises:
            FileNotFoundError: if the file does not exist at the specified path or if the specified version index is out of range
        """
        parts = split_path(path)

        directory_parts = parts[:-1]
        directory_path = "/" + "/".join(directory_parts)
        directory = resolve_path(self.root, directory_path)

        file_name = parts[-1]

        if file_name not in directory.files:
            raise FileNotFoundError(f"File {file_name} not found.")

        file_id = directory.files[file_name]
        metadata = self.metadata_store.get_metadata(file_id)

        versions = metadata.versions

        if version_index > len(versions) - 1:
            raise FileNotFoundError(f"File version of {file_name} not found.")

        versioned_file = versions[version_index]

        content_id = versioned_file.content_id

        return self.content_store.read_content(content_id)

    def search_results(self, word: str) -> list[str]:
        """
        searches for files that contain the specified word and returns a list of their paths.

        Args:
            word: the word to search for in the file contents

        Returns: a list of paths of the files that contain the specified word

        """
        matching_ids = self.search_index.search(word)

        results = []
        self._collect_search_results(self.root, matching_ids, results)

        return results

    def _collect_search_results(
        self, directory: DirectoryNode, matching_ids: Set[str], results: List[str]
    ):
        """
        utility function that recursively traverses the directory tree and collects the paths of files that match the search criteria.

        Args:
            directory: the current directory node being traversed
            matching_ids: a set of file IDs that match the search criteria
            results: a list to collect the paths of matching files
        """
        for file_name, file_id in directory.files.items():
            if file_id in matching_ids:
                file_path = self._build_directory_path(directory) + f"/{file_name}"
                results.append(file_path)

        for child in directory.subdirectories.values():
            self._collect_search_results(child, matching_ids, results)

    def export_state(self, file_path: str):
        """
        exports the current state of the file system to a JSON file at the specified path.

        Args:
            file_path: the path of the JSON file to export the state to
        """
        metadata_state = {}

        for (
            file_id,
            metadata,
        ) in self.metadata_store._store.items():
            serialized_versions = []

            for version in metadata.versions:
                serialized_versions.append(
                    {
                        "version_id": version.version_id,
                        "content_id": version.content_id,
                        "timestamp": version.timestamp.isoformat(),
                        "size": version.size,
                    }
                )

            metadata_state[file_id] = {
                "file_id": metadata.file_id,
                "name": metadata.name,
                "content_id": metadata.content_id,
                "size": metadata.size,
                "created_at": metadata.created_at.isoformat(),
                "modified_at": metadata.modified_at.isoformat(),
                "permissions": {
                    "read": metadata.permissions.read,
                    "write": metadata.permissions.write,
                    "delete": metadata.permissions.delete,
                },
                "versions": serialized_versions,
            }

        serialized_search_index = {}

        for (
            word,
            file_ids,
        ) in self.search_index._index.items():
            serialized_search_index[word] = list(file_ids)

        directory_data = serialize_directory(self.root)

        data = {
            "directory_tree": directory_data,
            "content_store": self.content_store._store,
            "cache_capacity": self.cache._capacity,
            "cache": dict(self.cache._cache),
            "search_index": serialized_search_index,
            "metadata_store": metadata_state,
        }

        with open(
            file_path,
            "w",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

    def load_state(
        self,
        file_path: str,
    ):
        """
        loads the state of the file system from a JSON file at the specified path.

        Args:
            file_path: the path of the JSON file to load the state from
        """
        with open(
            file_path,
            "r",
        ) as file:
            data = json.load(file)

        self.root = deserialize_directory(data["directory_tree"])

        self.content_store._store = data["content_store"]
        self.cache._capacity = data["cache_capacity"]
        self.cache._cache = OrderedDict(data["cache"])
        self.search_index._index = defaultdict(set)

        for (
            word,
            file_ids,
        ) in data["search_index"].items():
            self.search_index._index[word] = set(file_ids)

        self.metadata_store._store = {}

        for metadata in data["metadata_store"].values():
            versions = []

            for version_data in metadata["versions"]:
                version = FileVersion(
                    version_id=version_data["version_id"],
                    content_id=version_data["content_id"],
                    timestamp=datetime.fromisoformat(version_data["timestamp"]),
                    size=version_data["size"],
                )

                versions.append(version)

            permissions = Permissions(
                read=metadata["permissions"]["read"],
                write=metadata["permissions"]["write"],
                delete=metadata["permissions"]["delete"],
            )

            file_metadata = FileMetadata(
                file_id=metadata["file_id"],
                name=metadata["name"],
                content_id=metadata["content_id"],
                size=metadata["size"],
                created_at=datetime.fromisoformat(metadata["created_at"]),
                modified_at=datetime.fromisoformat(metadata["modified_at"]),
                permissions=permissions,
                versions=versions,
            )

            self.metadata_store.add_metadata(file_metadata)
