#!/usr/bin/env python3
import sys
import json
import ipaddress
import requests
import re
import time
from .texttable import Texttable
from .tabulate import tabulate
from decimal import Decimal


tt = Texttable()

class functions():

    # ------------------------------------------------------ #
    # Basic subnet calculator
    # ------------------------------------------------------ #

    def subnet_calc(prefix):

        ipi = ipaddress.ip_interface(prefix)
        table = ([['Address', ipi.ip],
        ['Mask', ipi.netmask],
        ['CIDR', ipi.with_prefixlen],
        ['Network', str(ipi.network).split('/')[0]],
        ['Broadcast', ipi.network.broadcast_address],
        ['Wildcard', str(ipi.with_hostmask).split('/')[1]],
        ['Usable hosts', int(ipi.network.num_addresses)-2]])
        return(tabulate(table, tablefmt="fancy_grid"))

    # ------------------------------------------------------ #
    # Mac Vendor Lookup
    # Uses the free API here: https://macvendors.com/api
    # Limited to 1,000 requests per day
    # ------------------------------------------------------ #

    def mac_lookup(mac_address):

        # valid mac address regexes
        regex = ("^([0-9A-Fa-f]{2}[:-])" +
                "{5}([0-9A-Fa-f]{2})|" +
                "([0-9a-fA-F]{4}\\." +
                "[0-9a-fA-F]{4}\\." +
                "[0-9a-fA-F]{4})$")
        
        # Compile the ReGex
        p = re.compile(regex)
    
        # If we have an empty string passed, return invalid
        if (mac_address == None):
            return "No MAC address provided"
    
        # Return info if our mac is in the correct         
        if(re.search(p, mac_address)):
            url = "https://api.macvendors.com/"
            mac_request  = requests.get(url + mac_address)
            table = ([['MAC Address', "Vendor"],
            [mac_address, mac_request.text]])
            return(tabulate(table, tablefmt="fancy_grid"))

        # If we don't have a valid mac, return the below
        else:
            return "Invalid MAC address provided"


    # ------------------------------------------------------ #
    # Rate limit calculator
    # Formulas gathered from here: 
    # https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_plcshp/configuration/15-mt/qos-plcshp-15-mt-book/qos-plcshp-oview.html
    # ------------------------------------------------------ #

    def rate_limit_calc(speed):

        normal_burst = int(speed) / 8 * 1.5
        extended_burst = 2 * int(normal_burst)
        tt.add_rows([['Function', 'Bits'],
                     ['Requested Speed', speed],
                     ["Normal Burst", normal_burst],
                     ["Extended Burst", extended_burst]],
                     header=True)
        return(tt.draw())

    def asn_lookup(asn):

        ipv4_list = []
        ipv6_list = []

        base_url = "https://api.bgpview.io/asn/"
        whois_request  = requests.get(base_url + asn)
        whois_json = whois_request.json()

        prefix_request  = requests.get(base_url + asn + "/prefixes")
        prefix_json = prefix_request.json()
        for ipv4_line in prefix_json["data"]["ipv4_prefixes"]:
            ipv4_list.append(ipv4_line["prefix"])
        for ipv6_line in prefix_json["data"]["ipv6_prefixes"]:
            ipv6_list.append(ipv6_line["prefix"])

        if len(ipv4_list) > 100:
            ipv4_list.insert(0, "### displaying first 50 prefixes - total: " + str(len(ipv4_list)) + " ###")
            ipv4_list = ipv4_list[:100]  
        if len(ipv6_list) > 100:
            ipv6_list.insert(0, "### displaying first 50 prefixes - total: " + str(len(ipv6_list)) + " ###")
            ipv6_list = ipv6_list[:100]

        tt.add_rows([["Name", whois_json["data"]["description_short"]],
                    ['ASN', asn],
                    ['Country', whois_json["data"]["country_code"]],
                    ['Email Contact', ', '.join(whois_json["data"]["email_contacts"])],
                    ['Abuse Contact', ', '.join(whois_json["data"]["abuse_contacts"])],
                    ['Traffic Estimation', whois_json["data"]["traffic_estimation"]],
                    ['IPv4 Prefixes', ', '.join(ipv4_list)],
                    ['IPv6 Prefixes', ', '.join(ipv6_list)]],
                    header=True)     

        return(tt.draw())


    def whois(ip_addr):
        base_url = "https://stat.ripe.net/data/whois/data.json?resource="
        whois_request  = requests.get(base_url + ip_addr)
        whois_json = whois_request.json()

        inetnum = whois_json["data"]["records"][0][0]["value"]
        netname = whois_json["data"]["records"][0][1]["value"]
        description = whois_json["data"]["records"][0][2]["value"]
        country_code = whois_json["data"]["records"][0][3]["value"]
        maintainer = whois_json["data"]["records"][0][7]["value"]
        prefix = whois_json["data"]["irr_records"][0][0]["value"]
        asn_desc = whois_json["data"]["irr_records"][0][1]["value"]
        asn = whois_json["data"]["irr_records"][0][2]["value"]


        tt.add_rows([["IP Address", ip_addr],
                    ['Prefix', inetnum],
                    ['Base Prefix', prefix],
                    ['Network Name', netname],
                    ['Description', description],
                    ['ASN', asn],
                    ['ASN Description', asn_desc],
                    ['Maintainer', maintainer],
                    ['Country Code', country_code]],
                    header=True)
        return(tt.draw())

    def convert(data, **kwargs):

        if "decimal_places" in kwargs:
            dp = "." + kwargs.get("decimal_places") + "f"
        else:
            dp = ".5f"

        number_only = int(re.search(r'\d+', data).group())

        if "petabyte" in data or "PB" in data:
            bit_converted_data = number_only * 9007199254740992
            unit = "Petabyte"
        elif "terabyte" in data or "TB" in data:
            bit_converted_data = number_only * 8796093022208
            unit = "Terabyte"
        elif "gigabyte" in data or "GB" in data:
            bit_converted_data = number_only * 8589934592
            unit = "Gigabyte"
        elif "megabyte" in data or "MB" in data:
            bit_converted_data = number_only * 8388608
            unit = "Megabyte"
        elif "kilobyte" in data or "KB" in data:
            bit_converted_data = number_only * 8192
            unit = "Kilobyte"
        elif "byte" in data or "B" in data:
            bit_converted_data = number_only * 8
            unit = "Byte"
        elif "petabit" in data or "Pb" in data:
            bit_converted_data = number_only * 1.1258998459315e+15
            unit = "Petabit"
        elif "terabit" in data or "Tb" in data:
            bit_converted_data = number_only * 1099511560222
            unit = "Terabit"
        elif "gigabit" in data or "Gb" in data:
            bit_converted_data = number_only * 1073741824
            unit = "Gigabit"
        elif "megabit" in data or "Mb" in data:
            bit_converted_data = number_only * 1048576
            unit = "Megabit"
        elif "kilobit" in data or "Kb" in data:
            bit_converted_data = number_only * 1024
            unit = "Kilobit"
        elif "bit" in data or "bit" in data:
            bit_converted_data = number_only
            unit = "Bit"

        table = ([[unit, number_only],
                    ['Bit', ((bit_converted_data))],
                    ['Byte', (bit_converted_data * 0.125)],
                    ['Kilobit', (bit_converted_data * 0.000977)],
                    ['Kilobyte', (bit_converted_data * 0.000122)],
                    ['Megabit', (bit_converted_data * 9.537e-7)],
                    ['Megabyte',( bit_converted_data * 1.1920928955078e-7)],
                    ['Gigabit', (bit_converted_data * 9.3132257462e-10)],
                    ['Gigabyte', (bit_converted_data * 1.1641532183e-10)],
                    ['Terabit', (bit_converted_data * 9.0949476e-13)],
                    ['Terabyte', (bit_converted_data * 1.1368684e-13)]])

        return(tabulate(table, tablefmt="fancy_grid", headers="firstrow", floatfmt=dp))


    def ip_reputation(ip):
        try:
            ipaddress.ip_address(ip)
            url = 'https://api.abuseipdb.com/api/v2/check'
            querystring = {
                'ipAddress': ip,
                'maxAgeInDays': '90',
                'verbose': True
            }
            headers = {
                'Accept': 'application/json',
                'Key': 'ed92bb00d541ccbff81586acaff856b71629df9de465d472c6579804f8acdc2a47947c6275bb3fad'
            }

            response = requests.request(method='GET', url=url, headers=headers, params=querystring)
            decodedResponse = json.loads(response.text)

            tt.add_rows([["IP Address", decodedResponse["data"]["ipAddress"]],
                        ['Domain', decodedResponse["data"]["domain"]],
                        ['ISP', decodedResponse["data"]["isp"]],
                        ['Country', decodedResponse["data"]["countryCode"]],
                        ['Abuse Score', decodedResponse["data"]["abuseConfidenceScore"]],
                        ['Total Reports (90 days)', decodedResponse["data"]["totalReports"]],
                        ['Last Reported', decodedResponse["data"]["lastReportedAt"]],
                        ['Latest Reports', decodedResponse["data"]["reports"][0]["comment"]]],
                        header=True)
            return(tt.draw())

        except ValueError:
            return("Incorrect IP address provided")


    def ssl_check(hostname):

        table_list = []

        url = 'https://api.ssllabs.com/api/v3/analyze?host=' + hostname
        response = requests.request(method='GET', url=url)
        decodedResponse = json.loads(response.text)

        count = 0
        while count < 20:
            tt = Texttable()
            response = requests.request(method='GET', url=url)
            decodedResponse = json.loads(response.text)
            if "IN_PROGRESS" in decodedResponse["status"]:
                count += 1
                # Sometimes the first response doesn't include "progress" as a key
                try:
                    tt.add_rows([["Host", decodedResponse["host"]],
                                ['Port', decodedResponse["port"]],
                                ['Protocol', decodedResponse["protocol"]],
                                ['Status', decodedResponse["status"]]],
                                header=True)
                    print(tt.draw())   
                    for x in decodedResponse["endpoints"]:
                        if "Ready" in x["statusMessage"]:
                            tt = Texttable() 
                            tt.add_rows([["IP Address", x["ipAddress"]],
                                        ['Status', x["statusMessage"]],
                                        ['Grade', x["grade"]],
                                        ['Progress', x["progress"]]]) 
                            print(tt.draw())
                        elif "In progress" in x["statusMessage"]:
                            tt = Texttable() 
                            tt.add_rows([["IP Address", x["ipAddress"]],
                                        ['Status', x["statusMessage"]],
                                        ['Current Step', x["statusDetails"]],
                                        ['Progress', x["progress"]]])
                            print(tt.draw()) 
                        elif "Pending" in x["statusMessage"]:       
                            tt = Texttable() 
                            tt.add_rows([["IP Address", x["ipAddress"]],
                                        ['Status', x["statusMessage"]]])
                            print(tt.draw())                                     
                        else:
                            print(x["statusMessage"])
                            pass
                    print("~" * 55)                                  
                    time.sleep(15)
                except Exception as e:
                    print("In progress")
                    print("~" * 55)
                    time.sleep(15)
            elif "READY" in decodedResponse["status"]:
                for x in decodedResponse["endpoints"]:
                    tt.add_rows([["Host", decodedResponse["host"]],
                                ['Port', decodedResponse["port"]],
                                ['Protocol', decodedResponse["protocol"]],
                                ['IP Address', x["ipAddress"]],
                                ['Grade', x["grade"]],
                                ['Warnings', x["hasWarnings"]]],
                                header=True)
                    table_list.append(tt)
                    tt = Texttable()
                return(table_list)       
