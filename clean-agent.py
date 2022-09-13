#!/usr/bin/env python

from src import main
from src import export_metrics

if __name__ == "__main__":
    metrics = main()
    print(metrics)
    export_metrics(metrics)
