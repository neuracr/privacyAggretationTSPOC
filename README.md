# POC for the Privacy-Preserving Aggregation of Time-Series Data paper from ndss2011

Implementating the summation protocol presented.

## Run the main experiment:

The main experiment features 20 participants who pick random values up. They send them to the aggregator and the aggregator sum them and print the result.

```bash
python3 main.py
```
## TODO

- implement the noise 
- make stats and graph
- implement new cases (evil participants, evil aggregator, ...)

## Run test from root:

```bash
python3 -m unittest poc.tests.test_ttp
```

safe primes http://oeis.org/A005385/b005385.txt
