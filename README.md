# Cleaning Agent Detection Script
This script is a way to capture the effectiveness of MBTA elevator sensors that detect the presence of urine and cleaning agents. 

## Functionality
This project is a command line script written in Python. 

The script reads 2 file paths as input (Sensor Data & Maintenance Request export), the files can be in CSV for XLSX format. 

The two files are compared to produce the following Metrics:

1. Count of True Positives

    * There is a sensor alert for cleaning agent detection and a corresponding cleaning work order.

2. Count of False Positives

    * There is a sensor alert for cleaning agent detection, but no corresponding cleaning work order.

3. Count of False Negatives

    * There is no sensor alert for cleaning agent detection, but there is a cleaning work order.

### Comparison Logic
_____
| Success Metric | Sensor Alert | Work Order | Timestamp |
|---|---|---|---|
| True Positive | Yes | Yes | Work Order timestamp is within 1 hour, after 1st Sensor Alert |
| False Positive | Yes | No | No work order within 1 hour, after 1st Sensor Alert |
| False Negative | No | Yes | No Sensor Alert within 1 hour, before Work Order timestamp |


## Developer Usage
This repo requires [python3](https://www.python.org/downloads/) to be installed and uses [pipenv](https://packaging.python.org/en/latest/tutorials/managing-dependencies/) to manage dependencies.

Install `pipenv`:
```
python3 -m pip install --user pipenv
```
Clone repo, inside of repo directory install pipenv dependencies:
```
pipenv install
```
Run script:
```
./clean-agent.py
```