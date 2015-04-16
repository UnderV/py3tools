# py3tools
Some handy system tools.

bash_exec example - returns 3 variables:
```python
#!/usr/bin/python3
from py3tools.bash_exec import bash_exec

(output, error_message, return_code) = bash_exec('ls -l')
```
