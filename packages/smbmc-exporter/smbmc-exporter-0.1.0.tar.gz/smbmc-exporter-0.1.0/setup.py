# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['smbmc_exporter']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'prometheus-client>=0.8.0,<0.9.0',
 'smbmc>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['smbmc-exporter = smbmc_exporter.console:main']}

setup_kwargs = {
    'name': 'smbmc-exporter',
    'version': '0.1.0',
    'description': 'Prometheus exporter for smbmc metrics',
    'long_description': 'smbmc-exporter\n==============\n\nPrometheus exporter for `smbmc <https://github.com/grawlinson/smbmc>`_ metrics.\n\nUsage\n-----\n\nVariables can be passed to the command-line interface via flags or environment variables.\n\n- ``--hostname``/``SMBMC_HOSTNAME``: Hostname of the SMBMC web-interface.\n- ``--username``/``SMBMC_USERNAME``: Username for the SMBMC web-interface.\n- ``--password``/``SMBMC_PASSWORD``: Password for the SMBMC web-interface.\n- ``--listen-port``/``LISTEN_PORT``: Port for daemon to listen on.\n- ``--listen-addr``/``LISTEN_ADDR``: Address for daemon to listen on.\n\nExample Metrics\n---------------\n\n::\n\n    # HELP smbmc_collector_collect_seconds Time spent to collect metrics from SMBMC\n    # TYPE smbmc_collector_collect_seconds summary\n    smbmc_collector_collect_seconds_count 3.0\n    smbmc_collector_collect_seconds_sum 1.0082290172576904\n    # HELP smbmc_collector_collect_seconds_created Time spent to collect metrics from SMBMC\n    # TYPE smbmc_collector_collect_seconds_created gauge\n    smbmc_collector_collect_seconds_created 1.6049614358040833e+09\n    # HELP smbmc_sensor_temperature_celsius Sensor Temperature\n    # TYPE smbmc_sensor_temperature_celsius gauge\n    smbmc_sensor_temperature_celsius{id="0",name="System Temp"} 27.0\n    smbmc_sensor_temperature_celsius{id="19",name="SAS2 FTemp1"} 29.0\n    # HELP smbmc_sensor_threshold_temperature_celsius Sensor Threshold - Temperature\n    # TYPE smbmc_sensor_threshold_temperature_celsius gauge\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="LNR"} -9.0\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="LC"} -7.0\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="LNC"} -5.0\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="UNC"} 80.0\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="UC"} 85.0\n    smbmc_sensor_threshold_temperature_celsius{id="0",type="UNR"} 90.0\n    # HELP smbmc_sensor_voltage_volts Sensor Voltage\n    # TYPE smbmc_sensor_voltage_volts gauge\n    smbmc_sensor_voltage_volts{id="1",name="12VCC"} 12.192\n    smbmc_sensor_voltage_volts{id="2",name="5VCC"} 5.027\n    smbmc_sensor_voltage_volts{id="3",name="3.3VCC"} 3.333\n    smbmc_sensor_voltage_volts{id="4",name="5VSBY"} 4.974\n    smbmc_sensor_voltage_volts{id="5",name="3.3VSBY"} 3.248\n    smbmc_sensor_voltage_volts{id="6",name="1.2VSB"} 1.251\n    smbmc_sensor_voltage_volts{id="7",name="1.5VSB"} 1.56\n    smbmc_sensor_voltage_volts{id="8",name="VBAT"} 3.112\n    smbmc_sensor_voltage_volts{id="23",name="SAS2 F5V"} 5.0\n    smbmc_sensor_voltage_volts{id="24",name="SAS2 F12V"} 12.0\n    # HELP smbmc_sensor_threshold_voltage_volts Sensor Threshold - Voltage\n    # TYPE smbmc_sensor_threshold_voltage_volts gauge\n    smbmc_sensor_threshold_voltage_volts{id="1",type="LNR"} 10.144\n    smbmc_sensor_threshold_voltage_volts{id="1",type="LC"} 10.272\n    smbmc_sensor_threshold_voltage_volts{id="1",type="LNC"} 10.784\n    smbmc_sensor_threshold_voltage_volts{id="1",type="UNC"} 12.96\n    smbmc_sensor_threshold_voltage_volts{id="1",type="UC"} 13.28\n    smbmc_sensor_threshold_voltage_volts{id="1",type="UNR"} 13.408\n    # HELP smbmc_sensor_fan_speed_rpm Fan Speed\n    # TYPE smbmc_sensor_fan_speed_rpm gauge\n    smbmc_sensor_fan_speed_rpm{id="9",name="FAN1"} 3500.0\n    # HELP smbmc_sensor_threshold_fan_speed_rpm Fan Speed - Threshold\n    # TYPE smbmc_sensor_threshold_fan_speed_rpm gauge\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="LNR"} 400.0\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="LC"} 600.0\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="LNC"} 800.0\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="UNC"} 25300.0\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="UC"} 25400.0\n    smbmc_sensor_threshold_fan_speed_rpm{id="9",type="UNR"} 25500.0\n    # HELP smbmc_sensor_status Sensor Status\n    # TYPE smbmc_sensor_status gauge\n    smbmc_sensor_status{id="0",name="System Temp"} 1.0\n    smbmc_sensor_status{id="1",name="12VCC"} 1.0\n    smbmc_sensor_status{id="9",name="FAN1"} 1.0\n    smbmc_sensor_status{id="10",name="FAN2"} 0.0\n    smbmc_sensor_status{id="19",name="SAS2 FTemp1"} 1.0\n    smbmc_sensor_status{id="23",name="SAS2 F5V"} 1.0\n    smbmc_sensor_status{id="24",name="SAS2 F12V"} 1.0\n    smbmc_sensor_status{id="27",name="PS2 Status"} 1.0\n    # HELP smbmc_pmbus_status Power Supply status\n    # TYPE smbmc_pmbus_status gauge\n    smbmc_pmbus_status{id="0"} 0.0\n    smbmc_pmbus_status{id="1"} 1.0\n    # HELP smbmc_pmbus_voltage_volts Power Supply Voltage\n    # TYPE smbmc_pmbus_voltage_volts gauge\n    smbmc_pmbus_voltage_volts{id="1",type="Input (AC)"} 242.0\n    smbmc_pmbus_voltage_volts{id="1",type="Output (DC)"} 12.1\n    # HELP smbmc_pmbus_current_amperes Power Supply Current\n    # TYPE smbmc_pmbus_current_amperes gauge\n    smbmc_pmbus_current_amperes{id="1",type="Input"} 0.359\n    smbmc_pmbus_current_amperes{id="1",type="Output"} 5.75\n    # HELP smbmc_pmbus_power_watts Power Supply Consumption\n    # TYPE smbmc_pmbus_power_watts gauge\n    smbmc_pmbus_power_watts{id="1",type="Input"} 86.0\n    smbmc_pmbus_power_watts{id="1",type="Output"} 69.0\n    # HELP smbmc_pmbus_temperature_celsius Power Supply Temperature\n    # TYPE smbmc_pmbus_temperature_celsius gauge\n    smbmc_pmbus_temperature_celsius{id="1",type="Input"} 37.0\n    smbmc_pmbus_temperature_celsius{id="1",type="Output"} 51.0\n    # HELP smbmc_pmbus_fan_speed_rpm Power Supply Fan Speed\n    # TYPE smbmc_pmbus_fan_speed_rpm gauge\n    smbmc_pmbus_fan_speed_rpm{id="1",type="Input"} 2858.0\n    smbmc_pmbus_fan_speed_rpm{id="1",type="Output"} 3847.0',
    'author': 'George Rawlinson',
    'author_email': 'george@rawlinson.net.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/grawlinson/smbmc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
