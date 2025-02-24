# jijzept_ai_agent

`jijzept_ai_agent` is a Jupyter AI module, a package
that registers additional model providers and slash commands for the Jupyter AI
extension.

## Requirements

- Python 3.8 - 3.12
- JupyterLab 4

## Install

To install the extension, execute:

```bash
pip install jijzept_ai_agent
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall jijzept_ai_agent
```

## Contributing

### Development install

```bash
cd jijzept-ai-agent
pip install -e "."
```

### Development uninstall

```bash
pip uninstall jijzept_ai_agent
```

#### Backend tests

This package uses [Pytest](https://docs.pytest.org/) for Python testing.

Install test dependencies (needed only once):

```sh
cd jijzept-ai-agent
pip install -e ".[test]"
```

To execute them, run:

```sh
pytest -vv -r ap --cov jijzept_ai_agent
```
