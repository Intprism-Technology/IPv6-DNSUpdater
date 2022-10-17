from bin import library as install

# Install library here
install.package('CloudFlare')
install.package('ipaddress')
# End install library here

from bin import getipv6
import time
import os
import json
import CloudFlare
import subprocess

# Function Cloudflare
def do_dns_update(zone_name, zone_id, ip_address, ip_address_type):
    """Cloudflare API DNS Update"""
    try:
        params = {'match':'all', 'type':ip_address_type}
        dns_records = cf.zones.dns_records.get(zone_id, params=params)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records %s - %d %s - api call failed' % ('dns_name', e, e))

    updated = False

    # update the record - unless it's already correct
    for dns_record in dns_records:
        old_ip_address = dns_record['content']
        old_ip_address_type = dns_record['type']
        
        if ip_address_type not in ['A', 'AAAA']:
            # we only deal with A / AAAA records
            continue

        if ip_address_type != old_ip_address_type:
            # only update the correct address type (A or AAAA)
            # we don't see this becuase of the search params above
            print('       => [IGNORED]: %s %s ; wrong address family' % (dns_record['name'], old_ip_address))
            continue

        if ip_address == old_ip_address:
            print('       => [UNCHANGED]: %s %s' % (dns_record['name'], ip_address))
            continue
        
        if(dns_record['name'] not in config["records"]):
            print('       => [SKIPPED]: %s %s' % (dns_record['name'], ip_address))
            continue

        proxied_state = dns_record['proxied']
    
        # Yes, we need to update this record - we know it's the same address type

        dns_record_id = dns_record['id']
        dns_record = {
            'name':dns_record['name'],
            'type':ip_address_type,
            'content':ip_address,
            'proxied':proxied_state
        }
        try:
            dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit('/zones.dns_records.put %s - %d %s - api call failed' % (dns_record['name'], e, e))
        print('       => [UPDATED]: %s %s -> %s' % (dns_record['name'], old_ip_address, ip_address))
        updated = True

    if updated:
        return

while True:
    # Update Repo
    update_repo = subprocess.check_output('cd /root/DNSUpdater && git pull', shell=True)
    print("[INFO] Application update status: {}".format(update_repo.decode("utf-8").strip()))
    if(getipv6.result() != "failed"):
        print("[INFO] Public IPv6: [{}]".format(getipv6.result()))
        print("[INFO] Reading config DNS Record")
        for path in os.listdir("config"):
            # check if current path is a file
            if os.path.isfile(os.path.join("config", path)):
                print("[INFO] Working on {} config...".format(path))
                # Cloudflare Driver
                try:
                    print("       [{}] Connect Cloudflare API...".format(path))
                    config = json.load(open(os.path.join("config", path)))
                    cf = CloudFlare.CloudFlare(email=config["cloudflare"]["email"], token=config["cloudflare"]["token"])
                    zones = cf.zones.get()
                    for zone in zones:
                        # print("zone_id=%s zone_name=%s" % (zone['id'], zone['name']))
                        do_dns_update(zone['name'], zone['id'], getipv6.result(), config["cloudflare"]["ip"])
                except:
                    print("[ERROR] Config file incorrect")
    else:
        print("[ERROR] Failed get IPv6... retry in 3s")
        time.sleep(3)
        continue
    print("[INFO] Complete, waiting in 30s")
    time.sleep(30)