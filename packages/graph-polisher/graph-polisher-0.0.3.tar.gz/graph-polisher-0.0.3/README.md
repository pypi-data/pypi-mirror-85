# Unclutterer

Unclutterer is a library that helps you clean your plotly figures. 
This library was inspired by the book "Storytelling with Data by Cole
Nussbaumer Knaflic (https://www.kobo.com/us/en/ebook/storytelling-with-data).

## Installation

```shell script
pip install unclutterer
```

## Testing

To test this project run:

```shell script
pytest
```

## Notebooks for examples

You can use this to see how the library modifies the plots. We are using 
[unnotebook](http://www.unnotebook.com/) to plot the examples. 

1. Build and push `notebook` image:

```bash
docker build . -t unclutterer
```

2. Run notebook

```shell script
docker-compose up notebook
```

or 

```bash
docker run --rm -it \
    -v /Users/rigo/Documents/Projects/notebooks/stock-predictions:/notebooks \
    -p 8899:8899 unclutterer
```


## Usage

...

## Deploying pip library

Build the pip library package to deploy to pip:

```shell script
python3 setup.py sdist bdist_wheel
```

Publish to pip. You can follow steps [here](https://docs.gitlab.com/ee/user/packages/pypi_repository/) 

Note that you will need to install twine and register your pypi. Usually in the file
`~/.pypirc`

```shell script
python3 -m twine upload --repository pypi dist/*
```
