# Association Rule Mining in Python, using the Apriori algorithm.

Requires Python 3. Dependencies managed using Poetry. Install Poetry using [instructions at python-poetry.org](https://python-poetry.org/docs/#installation)), then install dependencies with `poetry install`.

Run inside the virtual environment using `poetry run python main.py`.

Test with `poetry run pytest`.

Auto-format code to PEP8 using `./pyfmt`.

To run:

```
poetry run python main.py \
    --input datasets/supermarket.csv \
    --output supermarket-rules.txt \
    --min-confidence 0.8 \
    --min-support 0.05 \
    --min-lift 1.0
```
