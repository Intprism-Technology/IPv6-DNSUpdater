def result():
    import ipaddress
    import subprocess
    notGet = True
    while(notGet):
        try:
            direct_output = subprocess.check_output('ip a | grep "inet6 2"', shell=True)
            result_ip = direct_output.decode("utf-8").split("    inet6 ")[1].split("/")[0]
            notGet = False
        except:
            print("[WARN] Try to get IPv6")
    if(ipaddress.ip_address(result_ip).is_global != True):
        return "failed"
    return result_ip
