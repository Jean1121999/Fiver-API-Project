# Description: This API generates the average latency of each client wireless connected over the last hour
# You will be prompted to enter the Network for which you want the report for
# Author: Jean Aime Lukuka
# Date: March 15th, 2024

import meraki

# Enter your API key which can be generated (if not already) by going to your account in
# the top right corner > My profile
API_KEY = ''  # This API key is also a header in the url

dashboard = meraki.DashboardAPI(API_KEY)

# Parameters
organization_id = 00000  # Enter your organization ID
network_id = ''
timespan = 3600

count = 0
avg_latency = {}

# Get a list of all clients based on the timeframe
# Equivalent to going on the dashboard Network wide > Client. Except that the client page does not contain a timeframe
# of 1 hour
clients = dashboard.networks.getNetworkClients(network_id, total_pages=300, timespan=timespan)

# Average latency per clients for the last 3600 seconds or 1 hour
for x in clients:
    latency = dashboard.wireless.getNetworkWirelessLatencyHistory(network_id, clientId=f'{x['id']}',
                                                                  timespan=timespan, resolution=3600)
                                                                  # The resolution gets the average latency for that
                                                                  # timeframe

    # Only retrieves clients who reported high latency at some point within an hour
    if latency[0]['avgLatencyMs'] is not None:
        avg_latency[f'latency {count}'] = f'{latency[0]['avgLatencyMs']}'
        avg_latency[f'mac {count}'] = f'{clients[count]['mac']}'
        count += 1

# Displays the latency average for all clients connected in the last hour if latency entries are present
if len(avg_latency) is not 0:
    for x in range(int(len(avg_latency)/2)):
        print(f'Client: {avg_latency[f'mac {x}']}\n'
              f'Average Latency: {avg_latency[f'latency {x}']}')
else:
    print("No user were connected in the last hour")




