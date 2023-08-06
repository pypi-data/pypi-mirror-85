## fileargs

small CLI tool for executing commands and passing arguments based on config files

### example use
```
    fileargs -p params.yaml -- python some_file.py --some-param={{ path.to.value }}
```

Can be usefule when running stages in [DVC](https://dvc.org/) based on parameters in its `params.yaml`