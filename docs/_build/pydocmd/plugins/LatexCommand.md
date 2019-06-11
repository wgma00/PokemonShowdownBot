<h1 id="plugins.Latex.LatexCommand.Latex">Latex</h1>

```python
Latex(self)
```
Handles LaTeX related commands.

This class will take in commands of the form ".latex $equation$". It will
generate the corresponding LaTeX and upload it to the imgur image hosting.

Usage: .latex $[command]$
    - command: str, string with latex equation you would like to use.

Attributes:
    _client_id: client object that interacts with the imgur host
    _client: client object that interacts with the imgur host
    packages: default packages which are run at start

