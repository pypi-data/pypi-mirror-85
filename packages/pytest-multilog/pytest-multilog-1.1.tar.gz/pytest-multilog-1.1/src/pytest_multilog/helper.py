# Common test class with miscellaneous utilities and fixtures
import logging
import os
import shutil
from pathlib import Path
from typing import List, Union

import pytest
from _pytest.fixtures import FixtureRequest


@pytest.mark.usefixtures("logs")
class TestHelper:
    # Output folder
    @property
    def output_folder(self) -> Path:
        return self.root_folder / "out" / "tests"

    # Test folder (running)
    @property
    def test_folder(self) -> Path:
        return self.output_folder / "__running__" / self.worker / self.test_name

    # Test logs
    @property
    def test_logs(self) -> Path:
        return self.test_folder / "pytest.log"

    # Log content assertion
    def check_logs(self, expected: Union[str, List[str]]):
        # Get logs content
        with self.test_logs.open("r") as f:
            logs = f.read()
            to_check = expected if isinstance(expected, list) else [expected]

            # Verify all patterns are found in logs
            for expected_pattern in to_check:
                assert expected_pattern in logs, f"Expected pattern not found in logs: {expected_pattern}"

    # Test folder (final)
    @property
    def __test_final_folder(self) -> Path:
        return self.output_folder / self.test_name

    # Test name
    @property
    def test_name(self) -> str:
        return Path(os.environ["PYTEST_CURRENT_TEST"].split(" ")[0]).name.replace("::", "_").replace(".py", "")

    # Worker name in parallelized tests
    @property
    def worker(self) -> str:
        return os.environ["PYTEST_XDIST_WORKER"] if "PYTEST_XDIST_WORKER" in os.environ else "master"

    # Worker int index
    @property
    def worker_index(self) -> int:
        worker = self.worker
        return int(worker[2:]) if worker.startswith("gw") else 0

    # Per-test logging management
    @pytest.fixture
    def logs(self, request: FixtureRequest):
        # Set root folder
        self.root_folder = Path(request.config.rootdir).absolute().resolve()

        # Prepare test folder
        shutil.rmtree(self.test_folder, ignore_errors=True)
        shutil.rmtree(self.__test_final_folder, ignore_errors=True)
        self.test_folder.mkdir(parents=True, exist_ok=False)

        # Install logging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(
            level=logging.DEBUG,
            format=f"%(asctime)s.%(msecs)03d [{self.worker}/%(name)s] %(levelname)s %(message)s - %(filename)s:%(funcName)s:%(lineno)d",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=str(self.test_logs),
            filemode="w",
        )
        logging.info("-----------------------------------------------------------------------------------")
        logging.info(f"    New test: {self.test_name}")
        logging.info("-----------------------------------------------------------------------------------")

        # Return to test
        yield

        # Flush logs
        logging.info("-----------------------------------------------------------------------------------")
        logging.info(f"    End of test: {self.test_name}")
        logging.info("-----------------------------------------------------------------------------------")
        logging.shutdown()

        # Move folder
        shutil.move(self.test_folder, self.__test_final_folder)
        self.test_folder.parent.rmdir()
