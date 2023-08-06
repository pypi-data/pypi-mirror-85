# Copyright 2020 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""ETOS Client module."""
import logging

_LOGGER = logging.getLogger(__name__)


class ETOSClient:
    """Client for starting test suites in ETOS."""

    def __init__(self, etos):
        """Initialize ETOS client.

        :param etos: ETOS Library instance.
        :type etos: :obj:`etos_lib.etos.ETOS`
        """
        self.etos = etos
        self.test_execution = {}

    @property
    def data(self):
        """ETOS request data."""
        return {
            "artifact_identity": self.etos.config.get("identity").to_string(),
            "dataset": self.etos.config.get("dataset"),
            "iut_provider": self.etos.config.get("iut_provider"),
            "execution_space_provider": self.etos.config.get(
                "execution_space_provider"
            ),
            "log_area_provider": self.etos.config.get("log_area_provider"),
            "test_suite_url": self.etos.config.get("test_suite"),
        }

    def start(self, spinner):
        """Start ETOS test execution.

        :param spinner: Spinner text item.
        :type spinner: :obj:`Spinner`
        :return: Whether or not suite triggered correctly.
        :rtype: bool
        """
        spinner.info(str(self.data))
        generator = self.etos.http.retry(
            "POST", self.etos.debug.etos_api, timeout=30, json=self.data
        )
        response = None
        try:
            for response in generator:
                self.test_execution = response
                break
        except ConnectionError as exception:
            spinner.warning(str(exception))
            spinner.fail("Failed to trigger ETOS.")
            return False
        spinner.succeed("ETOS triggered.")
        return True

    @property
    def test_suite_id(self):
        """Test suite ID on TERCC."""
        recipe = self.test_execution.get(
            "EiffelTestExecutionRecipeCollectionCreatedEvent"
        )
        return recipe.get("meta", {}).get("id")
