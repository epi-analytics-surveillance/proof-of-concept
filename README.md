## simsurveillance
Python software for simulating, evaluating, and optimizing modes of disease monitoring.

## Installation
Installation of the software is possible via local pip. Download the files, and install using the following command:
```
pip install -e .
```
To perform the installation with optional support for inference via stan, use the following command:
```
pip install -e .[stan]
```
Note that installing stan on your computer may involve platform-specific requirements and dependencies which are not handled automatically by the pip install.

## Usage
For examples of usage, refer to the [examples](examples/) directory. For the full api documentation, see the [readthedocs]().

`simsurveillance` employs compartmental-type models of disease spread (SIRS).

```mermaid
graph LR
S((S)) --> I((I)) --> R((R)) --> S
```