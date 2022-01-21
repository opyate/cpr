import os
from typing import List

from whoosh import index
from whoosh.fields import SchemaClass, TEXT, ID, STORED
from whoosh.index import FileIndex
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher

from api.db import get_db_rows


class CPRSchema(SchemaClass):
    policy_id = ID(stored=True)
    description_text = TEXT(phrase=False)
    policy_title = STORED
    sectors = STORED


class Indexer:
    ix: FileIndex
    searcher: Searcher
    query_parser: QueryParser

    def __init__(self) -> None:
        """Initialises the indexer.

        If the index exists, then `docs` is ignored.
        If the index is new, it indexes `docs`.
        """
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
            self.ix = index.create_in("indexdir", CPRSchema)
            writer = self.ix.writer()
            docs = get_db_rows()
            for doc in docs:
                # to save space, we don't store the entire doc, as the spec
                # doesn't denote the `description_text` in the API response
                writer.add_document(
                    policy_id=doc.policy_id,
                    description_text=doc.description_text,
                    policy_title=doc.policy_title,
                    sectors=doc.sectors.split(';'),
                )

            writer.commit(optimize=True)
        else:
            self.ix = index.open_dir("indexdir")

        self.searcher = self.ix.searcher()
        self.query_parser = QueryParser("description_text", schema=self.ix.schema)

    def close(self):
        self.searcher.close()

    def search(self, keywords: List[str]):
        q = self.query_parser.parse(' '.join(keywords))
        results = self.searcher.search(q, limit=None)
        return results
