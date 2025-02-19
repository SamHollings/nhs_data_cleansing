# nhs-data-cleansing
![workflow_status](https://github.com/github/SamHollings/nhs-foundry-common/workflows/main.yml/badge.svg?event=push) ![Static Badge](https://img.shields.io/badge/status-development-blue)

## Description
This repo builds the `nhs-data-cleansing` python package, which contains generic Python functions (specifically using the PySpark library and data structures) for data cleansing. 

The functions can be seen in [`src`](src).

## Instalation
```bash
pip install nhs-data-cleansing
```

## Usage
Generally, simply add `nhs-data-cleansing` to your list of dependencies/requirements, then install the package.

> [!NOTE]
> It's best practice to specify a version of the library in your list of dependencies - then when 

### pip
Add `nhs-data-cleansing` to a `requirements.txt` file within the project, and then do `pip install -r requirements.txt`

### Foundry
Add `nhs-data-cleansing` to the `conda_recipe/meta.yml` file following the [Foundry "python libraries" guidance](https://www.palantir.com/docs/foundry/transforms-python/use-python-libraries)

## Contact
<add contact email address>

## Licence
Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. The documentation is © Crown copyright and available under the terms of the Open Government 3.0 licence.

## Contribution
If you want to help build and improve this package, see the [contributing guidelines](CONTRIBUTE.md) 

---
This readme has neem built in line with guidance from the [NHS Open Source Policy](https://github.com/nhsx/open-source-policy/blob/main/open-source-policy.md#b-readmes) and [govtcookiecutter](https://github.com/best-practice-and-impact/govcookiecutter/tree/main)
