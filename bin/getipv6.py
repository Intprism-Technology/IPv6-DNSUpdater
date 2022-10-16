def result():
    import ipaddress
    import os
    
    # try:
    #     result_ip = os.system('ip a | grep "inet6 2"')
    # except:
    #     os.system('apt update && apt install -y iproute2')
    #     try:
    #         result_ip = os.system('ip a | grep "inet6 2"')
    #     except Exception as e:
    #         print("Error {}").format(str(e))
    # result_ip = result_ip.split("inet6 ")[1].split("/")[0]
    # if(ipaddress.ip_address(result_ip).is_global != True):
    #     return "failed"
    # return result_ip
    return "2001:448a:50e1:92d3:f6b5:20ff:fe1e:1d35"