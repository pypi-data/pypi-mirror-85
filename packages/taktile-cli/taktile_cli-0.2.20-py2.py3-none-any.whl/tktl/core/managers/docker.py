import os
import time

import docker
import requests
from requests.exceptions import RequestException

from tktl.core.exceptions.exceptions import MissingDocker
from tktl.core.loggers import LOG

TESTING_DOCKERFILE = "Dockerfile.taktile-cli-testing"


class DockerManager:
    def __init__(self, path):
        try:
            self._client = docker.from_env()
            self._path = path
        except docker.errors.DockerException as err:
            raise MissingDocker from err

    def get_docker_file(self) -> str:
        with open(os.path.join(self._path, "Dockerfile")) as fp:
            return fp.read()

    def stream_logs(self, container) -> None:
        for line in container.logs(stream=True):
            LOG.trace(f"> {line.decode()}".strip())

    def patch_docker_file(self, output: str = TESTING_DOCKERFILE):
        """patch_docker_file
        
        Remove the line that does the profiling
        """
        with open(os.path.join(self._path, "Dockerfile")) as fp:
            contents = [
                line
                for line in fp.readlines()
                if "RUN python ${APPDIR}/profile_endpoints.py" not in line
            ]

        with open(os.path.join(self._path, output), "w") as fp:
            fp.writelines(contents)

    def remove_patched_docker_file(self, file_path: str = TESTING_DOCKERFILE):
        os.remove(os.path.join(self._path, file_path))

    def build_image(self, dockerfile: str = TESTING_DOCKERFILE) -> str:
        image = self._client.images.build(
            path=self._path, dockerfile=dockerfile, tag="taktile-cli-test"
        )
        return image[0].id

    def test_import(self, image_id: str):
        container = self._client.containers.run(
            image_id, "python -c 'from src.endpoints import tktl'", detach=True
        )
        self.stream_logs(container)

        status = container.wait()
        return status, container.logs()

    def test_unittest(self, image_id: str):
        container = self._client.containers.run(
            image_id, "python -m pytest ./user_tests/", detach=True
        )
        self.stream_logs(container)

        status = container.wait()
        return status, container.logs()

    def test_profiling(self, image_id: str):
        container = self._client.containers.run(
            image_id, "python /app/profile_endpoints.py", detach=True
        )
        self.stream_logs(container)

        status = container.wait()
        return status, container.logs()

    def test_integration(self, image_id: str):
        container = self._client.containers.run(
            image_id, detach=True, ports={"80/tcp": 8080}
        )
        try:
            for _ in range(5):
                try:
                    time.sleep(5)
                    resp = requests.get("http://localhost:8080/docs")
                    return resp, container.logs()
                except RequestException:
                    pass

            return None, container.logs()
        finally:
            container.kill()
