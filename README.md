# nhs_data_cleansing
![workflow_status](https://github.com/SamHollings/workflows/main.yml/badge.svg?event=push) ![Static Badge](https://img.shields.io/badge/status-development-blue) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
This repo builds the `nhs_data_cleansing` python package, which contains generic Python functions (specifically using the PySpark library and data structures) for data cleansing. 

The functions can be seen in [`src`](src).

ToDo: Add sphinx documentation (or something similar, automatically built)

## Instalation
```bash
pip install nhs_data_cleansing
```

## Usage
Generally, simply add `nhs_data_cleansing` to your list of dependencies/requirements, then install the package.

> [!NOTE]
> It's best practice to specify a version of the library in your list of dependencies - then when the package is updated, your existing work will not be affected.
> The verion numbers may need to be updated in the future, particularly if you want to use newer functionality.

### pip
Add `nhs_data_cleansing` to a `requirements.txt` file within the project, and then do `pip install -r requirements.txt`

### Foundry
Add `nhs_data_cleansing` to the `conda_recipe/meta.yml` file following the [Foundry "python libraries" guidance](https://www.palantir.com/docs/foundry/transforms-python/use-python-libraries)

## Contact
<add contact email address>

## Licence
Unless stated otherwise (and in keeping with the [NHS Open Source Policy](https://github.com/nhsx/open-source-policy/blob/main/open-source-policy.md#b-readmes)), the codebase is released under the MIT License. This covers both the codebase and any sample code in the documentation. The documentation is © Crown copyright and available under the terms of the Open Government 3.0 licence.

## Contribution
If you want to help build and improve this package, see the [contributing guidelines](CONTRIBUTE.md) 

---
This readme has neem built in line with guidance from the [NHS Open Source Policy](https://github.com/nhsx/open-source-policy/blob/main/open-source-policy.md#b-readmes) and [govtcookiecutter](https://github.com/best-practice-and-impact/govcookiecutter/tree/main)
