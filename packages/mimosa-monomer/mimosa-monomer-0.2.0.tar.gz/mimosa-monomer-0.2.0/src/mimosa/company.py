"""
Commands related to site key companies.

Some commands may not have been moved from sitekey.py yet.
"""
from pprint import pprint
from typing import List

import typer
from cerberus.validator import Validator
from halo import Halo

from mimosa import db
from mimosa.models import SiteKeyCompany
from mimosa.project import choose_project
from mimosa.theme import TyperStyles, HaloStyles

app = typer.Typer(help="Manage Stilt Site Key Companies")


@app.command("audit", help="Audit a single site key company for errors.")
def command_audit(
    site_key: str = typer.Option(..., prompt=True),
    company_id: str = typer.Option(..., prompt=True),
    skip_project: bool = False,
    audit_members: bool = False,
):
    audit(
        site_key=site_key,
        company_id=company_id,
        skip_project=skip_project,
        audit_members=audit_members,
    )


def audit(
    *,
    site_key: str,
    company_id: str,
    skip_project: bool = False,
    audit_members: bool = False,
) -> dict:
    """
    Audit a single site key company.
    """
    choose_project(skip=skip_project)
    company_data = db.get_company(site_key, company_id)

    v = Validator(SiteKeyCompany.schema)
    v.validate(company_data)
    errors = v.errors

    company_members = company_data.get("members")

    if audit_members is True and isinstance(company_members, list):
        errors = _audit_company_members(company_id, company_members, errors, site_key)

    _display_audit_results(site_key=site_key, company_id=company_id, errors=errors)

    return errors


def _audit_company_members(
    company_id: str, company_members: list, errors: dict, site_key: str
) -> dict:
    """
    Check the company members array against user's companyIDs in their permissions
    documents.
    """
    spinner = Halo(text_color=HaloStyles.spinner_text)
    spinner.start("Fetching uids...")
    users = db.query_all_sk_users(site_key=site_key)
    spinner.succeed()
    uids: List[str] = [user.id for user in users]

    # Get private documents.
    users_have_company_id = []
    spinner.start("Fetching user company ids...")
    for uid in uids:
        spinner.start(f"Fetching user company ids...{uid}")

        users_company = db.get_sk_user_permissions(site_key=site_key, uid=uid).get(
            "companyID"
        )
        if users_company == company_id:
            users_have_company_id.append(uid)
    spinner.succeed("Fetching user company ids...Done")
    # Compare differences from members array
    extra = set(company_members).difference(set(users_have_company_id))
    missing = set(users_have_company_id).difference(set(company_members))
    # Add results to a members entry in the errors dictionary, or create an entry.
    if len(extra) > 0 or len(missing) > 0:
        if errors.get("members") is None:
            errors["members"] = []
        if len(extra) > 0:
            errors["members"].append({"extra": extra})
        if len(missing) > 0:
            errors["members"].append({"missing": missing})

    return errors


@app.command("audit-all", help="Audit all companies in a site key")
def command_audit_all(
    site_key: str = typer.Option(..., prompt=True), skip_project: bool = False
):
    audit_all(site_key=site_key, skip_project=skip_project)


def audit_all(*, site_key: str, skip_project=False) -> dict:
    """Audit all companies in a site key"""
    choose_project(skip=skip_project)

    spinner = Halo(text_color=HaloStyles.spinner_text)
    spinner.start("Fetching data...")
    companies = db.query_all_site_key_companies(site_key=site_key)
    spinner.succeed()

    total_errors = dict()

    for company in companies:
        v = Validator(SiteKeyCompany.schema)
        v.validate(company.data)

        _display_audit_results(
            site_key=site_key, company_id=company.id, errors=v.errors
        )

        if v.errors != {}:
            total_errors[company.id] = v.errors

    return total_errors


def _display_audit_results(*, site_key: str, company_id: str, errors: dict) -> bool:
    site_key_text = typer.style(f"{site_key}", **TyperStyles.site_key)
    company_id_text = typer.style(f"{company_id}", **TyperStyles.company_id)
    if errors == {}:
        status_text = typer.style("passed", **TyperStyles.status, fg=typer.colors.GREEN)
        typer.echo(f"{site_key_text} {company_id_text}: {status_text}")
        return True
    else:
        status_text = typer.style("failed", **TyperStyles.status, fg=typer.colors.RED)
        typer.echo(f"{site_key_text} {company_id_text}: {status_text}")
        pprint(errors)
        return False


def main():
    app()


if __name__ == "__main__":
    main()
