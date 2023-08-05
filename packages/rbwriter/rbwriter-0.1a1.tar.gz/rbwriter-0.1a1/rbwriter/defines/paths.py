
"""
Global config for files/paths and directories
TODO: move paths into defines/configs.py
"""

import pathlib

# two times parent because we're two levels down in code
# (rbwriter/defines/paths.py)
ROOT = pathlib.Path(__file__).parent.parent

# this is relative from executing directory
DB_PATH = pathlib.Path("./db")
USER_DB_PATH = DB_PATH / "user.db"

COOKIE_PATH = pathlib.Path("./cookie")
USER_PATH = DB_PATH / "users"

TEMPLATE_PREFIX = pathlib.Path("templates/default/")

# absolute paths
PDF_TEMPLATE_ORIGIN_PATH = pathlib.Path(ROOT / TEMPLATE_PREFIX / "report_booklet_template_de.pdf").absolute()
TODOLIST_TEMPLATE_ORIGIN_PATH = pathlib.Path(ROOT / TEMPLATE_PREFIX / "todolist_template.json").absolute()

# relative paths
PDF_TEMPLATE_PATH = TEMPLATE_PREFIX / "report_booklet_template_de.pdf"
TODOLIST_TEMPLATE_PATH = TEMPLATE_PREFIX / "todolist_template.json"

# relative from user directory:
CONTENT_DB_PATH = "content.db"
TODOLIST_PATH = "todolist.json"
