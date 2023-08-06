"""
Colors and Styles.
"""

import typer


class HaloStyles:
    spinner_text = "blue"


class TyperStyles:
    site_key = {"bold": True}
    company_id = {"bold": True, "fg": typer.colors.YELLOW}
    status = {"bold": True}
