# -*- coding: utf-8 -*-

# Copyright 2015 Donne Martin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from __future__ import unicode_literals
from __future__ import print_function
import re
from .resource import Resource


class BucketNames(Resource):
    """Encapsulates the S3 bucket names resources.

    Attributes:
        * OPTION: A string representing the option for bucket names.
        * QUERY: A string representing the AWS query to list all bucket names.
        * resources: A list of bucket names.
        * log_exception: A callable log_exception from SawsLogger.
    """

    OPTION = '--bucket'
    QUERY = 'aws s3 ls'

    def __init__(self, log_exception):
        """Initializes BucketNames.

        Args:
            * log_exception: A callable log_exception from SawsLogger.

        Returns:
            None.
        """
        super(BucketNames, self).__init__(log_exception)

    def query_resource(self):
        """Queries and stores bucket names from AWS.

        Args:
            * None.

        Returns:
            The list of resources.
        """
        print('  Refreshing bucket names...')
        output = self._query_aws(self.QUERY)
        if output is not None:
            self.clear_resources()
            result_list = output.split('\n')
            for result in result_list:
                try:
                    result = result.split()[-1]
                    self.add_bucket_name(result)
                except:
                    # Ignore blank lines
                    pass

    def add_bucket_name(self, bucket_name):
        """Adds the bucket name to our bucket resources.

        Args:
            * bucket_name: A string representing the bucket name.

        Returns:
            None.
        """
        self.resources.extend([bucket_name])