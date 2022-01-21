import csv
import pathlib
from typing import Generator

from api.model import DBRow


def get_db_rows() -> Generator[DBRow, None, None]:
    csvfile = pathlib.Path(__file__, f'../../readonly_db/recruitment-task_1-full.csv').resolve()
    with open(csvfile, encoding='utf-8') as csvfile_fd:
        reader = csv.reader(csvfile_fd)
        next(reader, None)  # skip header
        for row in reader:
            db_row = DBRow(*row)
            yield db_row
