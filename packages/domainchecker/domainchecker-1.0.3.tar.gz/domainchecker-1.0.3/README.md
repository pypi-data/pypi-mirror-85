# onamae-domain-check

A python module that provides check if the domain is available, via Onamae.com Status API

# Requirements

`python>=3.7`

# Usage

Install:

```
pip install domainchecker
```

Example:

```python
print(check_domain('google', ['.com', '.jp']))
# output: {'google.com': False, 'google.jp': False}
```