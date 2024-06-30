import os
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from nornir_netmiko.tasks import netmiko_send_command

nr = InitNornir(config_file="../nornir_data/config.yaml")

def get_tunnel_type(task, interface):
    output_ikev2 = task.run(
        task=netmiko_send_command,
        command_string=f"show crypto ikev2 sa | include {interface}"
    )
    if output_ikev2.result:
        return "ikev2"

    output_ikev1 = task.run(
        task=netmiko_send_command,
        command_string=f"show crypto isakmp sa | include {interface}"
    )
    if output_ikev1.result:
        return "ikev1"
    
    return "unknown"

def get_tunnel_info(task, interface, tunnel_type):
    phase1_status = "unknown"
    phase2_status = "unknown"
    uptime = "unknown"

    if tunnel_type == "ikev2":
        phase1_output = task.run(
            task=netmiko_send_command,
            command_string="show crypto ikev2 sa"
        )
        phase2_output = task.run(
            task=netmiko_send_command,
            command_string="show crypto ipsec sa"
        )
    elif tunnel_type == "ikev1":
        phase1_output = task.run(
            task=netmiko_send_command,
            command_string="show crypto isakmp sa"
        )
        phase2_output = task.run(
            task=netmiko_send_command,
            command_string="show crypto ipsec sa"
        )

    if phase1_output.result:
        phase1_status = "Ready" if "READY" in phase1_output.result else "Not Ready"

    if phase2_output.result:
        phase2_status = "Ready" if "ACTIVE" in phase2_output.result else "Not Ready"

    tunnel_uptime_output = task.run(
        task=netmiko_send_command,
        command_string=f"show interfaces {interface} | include line protocol"
    )
    if tunnel_uptime_output.result:
        uptime = tunnel_uptime_output.result.strip()

    return [tunnel_type, phase1_status, phase2_status, uptime]

def check_interfaces(task):
    result = task.run(task=napalm_get, getters=["interfaces"])
    interfaces = result.result['interfaces']

    for interface, details in interfaces.items():
        description = details.get("description", "").lower()
        if "ISP" in description:
            print(f"{interface} is an ISP interface")
        elif "tunnel" in description:
            #print(f"{interface} is a tunnel interface")
            tunnel_type = get_tunnel_type(task, interface)
            tunnel_info = get_tunnel_info(task, interface, tunnel_type)
            print(f"Tunnel Information for {interface}: {tunnel_info}")

result = nr.run(task=check_interfaces)

#print_result(result)



