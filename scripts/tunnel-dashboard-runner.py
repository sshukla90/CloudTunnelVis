import os
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command
from rich import print as rprint


nr = InitNornir(config_file="../nornir_data/config.yaml")

def get_tunnel_info(task):
    tunnel_info= task.run(task=send_command, command="sh crypto session detail")
    structurd_output = tunnel_info.scrapli_response.textfsm_parse_output()
    rprint(structurd_output)

def get_interface_status():
    pass

def get_bgp_info():
    pass
result = nr.run(task=get_tunnel_info)
print_result(result)



