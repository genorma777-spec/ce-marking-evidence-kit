# CE marking evidence kit

Use this kit to connect each applicable product requirement to a specific configuration, assessment method and evidence record. It is intended for manufacturers and quality teams preparing or reviewing a technical file.

## Start with a product and its requirements

1. Copy [the blank evidence matrix](evidence-matrix.csv) for a project. Identify the model or configuration and the applicable EU legislation before deciding what evidence is needed.
2. For every requirement, add the legal reference and the method used. For a harmonised standard, record the exact edition and check any restrictions or applicable dates. If the technical method is different, describe it in the assessment-method field.
3. Link to the evidence file and its revision. Assign the review to an owner, leave gaps open and give each gap a review date. Consult [the worked example](example-evidence-matrix.csv) for fictional sample rows.
4. Review the alert list with the people who own the evidence. Keep the controlled records in your own internal system.

## Check the CSV locally

Run with Python 3. The checker has no third-party dependencies and sends no data.

```sh
python check_matrix.py example-evidence-matrix.csv
```

An exit status of 1 means at least one row needs attention. An exit status of 2 means the input could not be read or its format is invalid. The script checks record completeness and basic formatting. The assessment and determination of conformity remain with the responsible team.

| Status | What the kit expects |
| --- | --- |
| Pending | A named owner, a gap or next action, and a review date |
| Reviewed | A documented method, evidence reference, evidence revision, named owner and review date |
| Not applicable | A reason and a named owner |

Example identifiers and documents are fictional and are not a product assessment.

## Further reading

- [CE Marking Evidence Checklist for EN Standards](https://european-standards.com/ce-en-compliance-guide/)
- [Your Europe guidance on CE marking](https://europa.eu/youreurope/business/product-rules-compliance/general-product-compliance/ce-marking/index_en.htm)
- [European Commission harmonised standards index](https://single-market-economy.ec.europa.eu/single-market/goods/european-standards/harmonised-standards_en)
