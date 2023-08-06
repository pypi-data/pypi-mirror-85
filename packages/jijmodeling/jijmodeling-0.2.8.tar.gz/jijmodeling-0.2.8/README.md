# Jij-Modeling

## Document 生成

- Module ごとの rst ファイルの生成
```
sphinx-apidoc -f -e -o ./docs/source/module_doc/ .
```

- htmlへのコンパイル
```
sphinx-build ./docs/source/ ./docs/build/
```

## For jijmodeling commiter

### pipenv virtual enviroment
```
$ pipenv update
$ pipenv shell
```

## Run all test

Execution of all test files under `tests`.
```
$ python -m unittest discover tests
```

## About Deploy

We use GitHub Action. see `./github/workflows`.

