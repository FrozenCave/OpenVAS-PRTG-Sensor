import json
import sys
import requests

from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from paesslerag_prtg_sensor_api.sensor.units import ValueUnit

def make_request(url):
    try:
        response = requests.get(url)
        return response.text.strip()
    except requests.RequestException as e:
        return str(e)

if __name__ == "__main__":
    try:
        target_url = "http://localhost:8000"
        response_text = make_request(target_url)

        try:
            response_value = int(response_text)
        except ValueError:
            response_value = None

        csr = CustomSensorResult(text="OpenVAS Sensor")

        if response_value is not None:
            csr.add_primary_channel(name="Out of Range",
                                    value=response_value,
                                    unit=ValueUnit.CUSTOM,
                                    is_float=False,
                                    is_limit_mode=True,
                                    limit_min_error=0,
                                    limit_max_error=12,
                                    limit_error_msg="Status out of range")

            csr.add_channel(name="Low Priority Vulnerability",
                                value=response_value,
                                unit=ValueUnit.CUSTOM,
                                is_float=False, 
                                is_limit_mode=True,
                                limit_min_warning=5.9,
                                limit_warning_msg="Low Priority Vulnerability found")
                
                
            csr.add_channel(name="Crucial Vulnerability",
                                value=response_value,
                                unit=ValueUnit.CUSTOM,
                                is_float=False,
                                is_limit_mode=True,
                                limit_max_error=6,
                                limit_error_msg="Crucial Vulnerability found")

            if response_value == 'OK':
                csr.text = "Sensor is green"

        else:
            csr.error = "Invalid response: " + response_text

        print(csr.json_result)

    except requests.RequestException:
        csr = CustomSensorResult(text="OpenVAS Endpoint not reachable")
        csr.error = "OpenVAS Endpoint not reachable"
        print(csr.json_result)

    except Exception as e:
        csr = CustomSensorResult(text="Python Script execution error")
        csr.error = "Python Script execution error: %s" % str(e)
        print(csr.json_result)
