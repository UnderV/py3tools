# py3tools
Some handy system tools.

**shell_exec** example:
```python
#!/usr/bin/python3
from py3tools.shell_exec import shell_exec

(output, error_message, return_code) = bash_exec('ls -l')
```
Returns 3 variables:
output - contains command output
error_message - contains error message or empty string
return_code - contains return code
