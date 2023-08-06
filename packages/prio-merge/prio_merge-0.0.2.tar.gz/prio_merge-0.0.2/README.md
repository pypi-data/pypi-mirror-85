# Prio merge

Merge two dictionaries on a deep level with one taking precedent over another,
and by using a few rules:

If keys exist in just one of the dictionaries, it will be merged in the final dictionary

If two keys exist in the same nested depth, one of these things will happen
* if the values have different types, prioritized dict value will take remain
* if both values are lists, they will be combined according by appending the non-prioritized list to the other and then removing duplicates by casting to a list. *This means that list order can not be guaranteed* _It also means that any list will end the recursive nature of the merge_
* if both values are dicts, the keys will be combined recursively using these rules
* otherwise take the value from the prioritized dictionary

## Usage
```python
from prio_merge import prio_merge

prio_dict = {}
```
