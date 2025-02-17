#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Module in charge of running the queries against
the session.

This is useful to centralise the running logic
and manage behavior such as timeouts.
"""
from typing import Union

from sqlalchemy.orm import DeclarativeMeta, Query, Session
from sqlalchemy.orm.util import AliasedClass


class QueryRunner:
    """
    Handles the query runs and returns the results
    to the caller.

    The goal of this class is abstract a bit
    how to get the query results. Moreover,
    we can then wrap it up with a timeout
    to make sure that methods executed from this class
    won't take more than X seconds to execute.
    """

    def __init__(
        self,
        session: Session,
        table: DeclarativeMeta,
        sample: Union[DeclarativeMeta, AliasedClass],
    ):
        self._session = session
        self._table = table
        self._sample = sample

    def _build_query(self, *entities, **kwargs) -> Query:
        return self._session.query(*entities, **kwargs)

    def _select_from_sample(self, *entities, **kwargs):
        return self._build_query(*entities, **kwargs).select_from(self._sample)

    def select_first_from_table(self, *entities, **kwargs):
        return self._build_query(*entities, **kwargs).select_from(self._table).first()

    def select_all_from_table(self, *entities, **kwargs):
        return self._build_query(*entities, **kwargs).select_from(self._table).all()

    def select_first_from_sample(self, *entities, **kwargs):
        return self._select_from_sample(*entities, **kwargs).first()

    def select_all_from_sample(self, *entities, **kwargs):
        return self._select_from_sample(*entities, **kwargs).all()

    @staticmethod
    def select_first_from_query(query: Query):
        return query.first()

    @staticmethod
    def select_all_from_query(query: Query):
        return query.all()
