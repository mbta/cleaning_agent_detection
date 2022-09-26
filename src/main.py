import datetime
import logging
from time import time

from .agent_lib import pull_sense_file
from .agent_lib import pull_clean_report_file
from .agent_lib import list_to_dict
from .agent_lib import Metric
from .agent_lib import export_metrics

logging.getLogger().setLevel("INFO")


def main() -> Metric:
    metrics = Metric()

    (sense_data, sense_dt_min, sense_dt_max) = pull_sense_file()
    if len(sense_data) == 0:
        logging.error(f"No valid sensor records found in file.")
        return metrics
    # create set of tuples containing zone and elevator combinations found
    # in sensor data
    # cleaning records not containing these combinations will be dropped 
    sensor_locations = set((record.zone, record.elevator) for record in sense_data)

    (clean_data, clean_dt_min, clean_dt_max) = pull_clean_report_file(sensor_locations)
    if len(clean_data) == 0:
        logging.error(f"No relevant maintenance records found in file.")
        return metrics

    # find overlapping datetime period for sensor and maintenance data
    dt_min = max(sense_dt_min, clean_dt_min) - datetime.timedelta(seconds=60 * 60)
    dt_max = min(sense_dt_max, clean_dt_max) + datetime.timedelta(seconds=60 * 60)

    logging.info(f"Overlapping time period is from {dt_min.strftime('%b %d, %Y')} to {dt_max.strftime('%b %d, %Y')}")

    # convert list of records into dictionaries
    # limit records in dictionaries to overlapping datetime period
    sense_data = list_to_dict(sense_data, dt_min, dt_max)
    clean_data = list_to_dict(clean_data, dt_min, dt_max)

    # loop through sensor data to find true_positive counts and false_positive count
    for zone, zone_data in sense_data.items():
        for elevator, elevator_data in zone_data.items():
            for record in elevator_data:
                try:
                    match_found = False
                    for clean_record in clean_data[zone][elevator]:
                        time_diff = (clean_record.dt - record.dt).total_seconds()
                        if time_diff >= 0 and time_diff <= 60 * 60:
                            clean_record.has_alert = True
                            # avoid double counting but tags multiple records in detection window
                            if match_found is False:
                                metrics.true_positive.append((record, clean_record))
                                match_found = True
                        elif time_diff > 60 * 60:
                            break
                # this should only be KeyError's but left as general Exception for now...
                except Exception as e:
                    pass
                if match_found is False:
                    metrics.false_positive.append(record)

    # loop through maintenance cleaning records to find false_negatie count
    for zone_data in clean_data.values():
        for elevator_data in zone_data.values():
            for record in elevator_data:
                if record.has_alert is False:
                    metrics.false_negative.append(record)

    return metrics
