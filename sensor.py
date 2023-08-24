import json
import requests
from paesslerag_prtg_sensor_api.sensor.result import CustomSensorResult
from paesslerag_prtg_sensor_api.sensor.units import ValueUnit

def make_request(url):
    try:
        response = requests.get(url, verify=False)
        data = json.loads(response.text.strip())
        scores = [float(item.get("score", 0)) for item in data]
        highest_score = max(scores)
        return highest_score
    except requests.RequestException as e:
        return str(e)

def create_res():
    try:
        target_url = "https://192.168.31.52/api/results"
        response_text = make_request(target_url)

        try:
            response_value = int(response_text)
        except ValueError:
            response_value = None

        csr = CustomSensorResult(text="No Vulnerabilties found")

        if response_value is not None:
            csr.add_primary_channel(name="Low Priority Vulnerability",
                                value=response_value,
                                unit=ValueUnit.CUSTOM,
                                is_float=True, 
                                is_limit_mode=True,
                                limit_max_warning=2,
                                limit_warning_msg="Low Priority Vulnerability found")
                      
            csr.add_channel(name="Crucial Vulnerability",
                                value=response_value,
                                unit=ValueUnit.CUSTOM,
                                is_float=True,
                                is_limit_mode=True,
                                limit_max_error=5.9,
                                limit_error_msg="Crucial Vulnerability found")

        else:
            csr.error = "Invalid response: " + response_text

        return csr.json_result

    except requests.RequestException:
        csr = CustomSensorResult(text="OpenVAS Endpoint not reachable")
        csr.error = "OpenVAS Endpoint not reachable"
        return csr.json_result

    except Exception as e:
        csr = CustomSensorResult(text="Python Script execution error")
        csr.error = "Python Script execution error: %s" % str(e)
        return csr.json_result

if __name__ == "__main__":
    output = create_res()

    print(output)