# py3tools
Some handy system tools.

**bash_exec** example:
```python
#!/usr/bin/python3
from py3tools.bash_exec import bash_exec

(output, error_message, return_code) = bash_exec('ls -l')
```
Returns 3 variables:
output - contains command output
error_message - contains error message or empty string
return_code - contains return code
