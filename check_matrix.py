"""Check completion of a local CE marking evidence matrix CSV."""
import argparse
import csv
from datetime import date
from pathlib import Path
import re
import sys

COLUMNS = (
    "requirement_id", "product_configuration", "legal_reference",
    "assessment_method", "standard_edition", "evidence_reference",
    "evidence_revision", "owner_role", "status", "next_action_or_reason",
    "review_date",
)
COMMON = ("requirement_id", "product_configuration", "legal_reference", "owner_role")
REQUIRED = {
    "pending": ("next_action_or_reason", "review_date"),
    "reviewed": ("assessment_method", "evidence_reference", "evidence_revision", "review_date"),
    "not applicable": ("next_action_or_reason",),
}


def check(path):
    issues = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, strict=True)
        if tuple(reader.fieldnames or ()) != COLUMNS:
            raise ValueError("Use the header from evidence-matrix.csv.")
        for raw in reader:
            line = reader.line_num
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError(f"Record ending on line {line} has the wrong number of fields.")
            row = {key: value.strip() for key, value in raw.items()}
            if not any(row.values()):
                continue
            ref = row["requirement_id"]
            location = f"Line {line}" + (f" ({ref})" if ref else "")
            key = (ref.casefold(), row["product_configuration"].casefold())
            if ref and key in seen:
                issues.append(f"{location}: duplicate ID for this configuration.")
            if ref:
                seen.add(key)
            status = row["status"].casefold()
            if status not in REQUIRED:
                issues.append(f"{location}: status must be Pending, Reviewed or Not applicable.")
            missing = [column for column in COMMON + REQUIRED.get(status, ()) if not row[column]]
            if missing:
                issues.append(f"{location}: missing " + ", ".join(missing) + ".")
            if status == "pending":
                issues.append(f"{location}: open evidence gap — {row['next_action_or_reason'] or 'action needed'}.")
            if row["review_date"]:
                try:
                    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", row["review_date"]):
                        raise ValueError
                    date.fromisoformat(row["review_date"])
                except ValueError:
                    issues.append(f"{location}: review_date must be a valid YYYY-MM-DD date.")
    return issues, len(seen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    try:
        issues, records = check(args.matrix)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        print(f"Cannot check the matrix: {error}", file=sys.stderr)
        return 2
    if not records and not issues:
        print("Empty matrix. Add evidence records before review.")
    elif not issues:
        print(f"{records} record(s) checked. No completeness issues found.")
    for issue in issues:
        print(issue)
    return int(bool(issues))


if __name__ == "__main__":
    sys.exit(main())
