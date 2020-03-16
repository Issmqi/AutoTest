import re
value='hello World'
result = re.findall("\${(.*?)}\$", value)
print(result)