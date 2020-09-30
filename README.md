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