import os
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_scrapli.tasks import send_command
from rich import print as rprint
from tabulate import tabulate


nr = InitNornir(config_file="../nornir_data/config.yaml")

def get_tunnel_info(task):
    tunnel_info= task.run(task=send_command, command="sh crypto session detail")
    structurd_output = tunnel_info.scrapli_response.textfsm_parse_output()
    #rprint(structurd_output)

    table_data = []

    for item in structurd_output:
        table_data.append([
            task.host,             # Hostname
            item.get('interface', ''),
            item.get('session_status', ''),
            item.get('uptime', ''),
            item.get('peer', ''),
            item.get('ikev1_status', ''),
            item.get('remote_ip', '')
        ])
    headers = ["Host", "Interface", "Session Status", "Uptime", "Peer", "IKEv1 Status", "Remote IP"]
    rprint(tabulate(table_data, headers=headers, tablefmt="pretty"))

result = nr.run(task=get_tunnel_info)
#print_result(result)



