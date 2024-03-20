# Description: This API generates a percentage of the number of failed connections over the last hour
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

tot_conn = 0
tot_fail_conn = 0

# Get a list of all clients based on the timeframe
# Equivalent to going on the Meraki dashboard, and then Network wide > Client. Except that the client page does not
# contain a timeframe of 1 hour
clients = dashboard.networks.getNetworkClients(network_id, total_pages=300, timespan=timespan)

for x in clients:

    connection_event = dashboard.wireless.getNetworkWirelessClientConnectivityEvents(network_id, timespan=timespan,
                                                                                     clientId=f'{x['id']}')
    # Additions all connections
    tot_conn += (len(connection_event))

    # Retrieves the failed connections only
    for y in connection_event:
        if y['subtype'] == 'failed':
            tot_fail_conn += 1  # Additions all the failed connections

# Calculate the percentage of failed connections rounded up to the second decimal
failed_conn_pct = round(((tot_fail_conn * 100) / tot_conn), 2)

# Prints the percentage
print(f"Percentage of failed connection over the last hour:\n"
      f"{failed_conn_pct}%")






