from __future__ import annotations
import json
from time import sleep
from typing import List, Dict
from qtcurate.qt import Qt
from qtcurate.exceptions import QtArgumentError, QtJobError
from qtcurate.connect import connect

description = "title"
files = "files"


class Job:
    def __init__(self):
        self.headers = {"X-API-Key": Qt.api_key}
        self.temp_dict = dict()
        self.url = Qt.url
        self.model_id = None
        self.id = None

    def __repr__(self):
        return f"{self.id}"

    def get_id(self) -> str:
        """Get job id"""

        return str(self.id)

    def set_description(self, title: str) -> Job:
        """Create title for Job"""

        if isinstance(title, str):
            self.temp_dict[description] = title
        else:
            raise QtArgumentError("Argument type error: String is expected as description")
        return self

    def with_documents(self, list_of_files: List) -> Job:
        """Create a list of existing files"""

        if isinstance(list_of_files, list):
            self.temp_dict[files] = list_of_files
        else:
            raise QtArgumentError("Argument type error: Expected list of file IDs")
        return self

    def with_model(self, model_id: str) -> Job:
        """Add model to Job"""

        if isinstance(model_id, str):
            self.model_id = model_id
        else:
            raise QtArgumentError("Argument type error: Expected string as model ID")
        return self

    def create(self) -> Dict:
        """Creating a new Job"""
        self.headers["Content-Type"] = "application/json"
        if description not in self.temp_dict:
            raise QtJobError("Job error: Description is mandatory. Please add description with set_description method")
        if files not in self.temp_dict:
            raise QtJobError("Job error: Please add list of documents with with_documents method ")

        res = connect("post", f"{self.url}search/new/{self.model_id}", self.headers,  "data", json.dumps(self.temp_dict))
        self.id = res.json()['id']
        del self.headers['Content-Type']
        return res.json()

    def fetch(self, job_id: str) -> Dict:
        """ Fetch job where job_id is existing ID"""

        self.headers["Content-Type"] = "application/json"
        if not isinstance(job_id, str):
            raise QtArgumentError("Argument type error: String is expected as job_id")
        res = connect("get", f"{self.url}search/config/{job_id}", self.headers)
        self.id = res.json()['id']
        del self.headers['Content-Type']
        return res.json()

    def delete(self, job_id: str) -> bool:
        """Delete data container"""

        if not isinstance(job_id, str):
            raise QtArgumentError("Argument type error: String is expected as job_id")
        res = connect("delete", f"{self.url}search/{job_id}", self.headers)
        return res.ok

    def progress(self, job_id: str = None) -> Dict:
        """Show progress for submitted for job"""
        url_path = "progress"
        if job_id is not None:
            if isinstance(job_id, str):
                url_path = f"{url_path}/{job_id}"
            else:
                raise QtArgumentError("Expected string")
        res = connect("get", f"{self.url}search/{url_path}", self.headers)
        return res.json()

    def wait_for_completion(self) -> None:
        """Wait for completion job"""

        percentage = 0
        while percentage < 100:
            result = self.progress(self.id)
            percentage = result["progress"]
            print(f"Search progress {percentage}%")
            if percentage < 100:
                sleep(1)
        sleep(3)
