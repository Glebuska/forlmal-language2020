# Formal-language2020
Repository for homeworks
#### Status on last pull request:<br>
<img src ="https://github.com/Glebuska/formal-language2020/workflows/Pytest/badge.svg"><br>

## To install: <br>
```
conda install -c conda-forge --file requirements.conda.txt
pip install -r requirements.pip.txt
```

## To run: <br>
```
python3 src/main.py --graph_path<path_to_graph> --regex_path<path_to_regex> *optional arguments* --out<path_to_output_vertices> --to<path_to_input_vertices>

```
See help information: <br>
``` python3 src/main.py -h ```

## To run tests: <br>
```
git clone https://github.com/Glebuska/formal-language2020
install all libraries
python3 -m pytest 
```

# QUERY Language Syntax: <br>

## To run it:
```
python3 src/query_language.py --script<command> --language<path_to_language txt>

```
See help information: <br>
``` python3 src/query_language.py -h ```

## Syntax:
```
script := eps | list of stmt
stmt := connect to <name> | select <exrp> from <graph>
graph := query <pattern> | <graph> intetsect <graph> | <name>
expr := edges | count edges
pattern := list of pattern | <star> | <name> | <plus> | <alt> pattern pattern | option pattern
star := *
plus := +
alt := |
option := ?
edges := e d g e s
connect := c o n n e c t
select := s e l e c t
from := f r o m
intersect := i n t e r s e c t
count := c o u n t
query := q u e r y
to := t o
name := (NAME)* | (WORD | NUM)*
WORD (WORD)*
 
```
## Example <br>
```
select edges from g1 intersect g2
```
```
connect to db1
```

```
select edges from query * | query + db | query db1
```
```
select count edges from db
```
