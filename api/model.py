import collections
from typing import List

from pydantic import BaseModel

# represents a row in the CSV database
DBRow = collections.namedtuple(
    "DBRow", ["policy_id", "policy_title", "sectors", "description_text"]
)


class Match(BaseModel):
    similarity: float
    policyId: int
    policyTitle: str
    sectors: List[str] = []


class Matches(BaseModel):
    matches: List[Match] = []
