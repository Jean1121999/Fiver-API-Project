# Description: This API generates the average Signal strength for each user per network
# You will be prompted to enter the Network for which you want the report for
# Author: Jean Aime Lukuka
# Date: March 14th, 2024

import meraki

# Enter your API key which can be generated (if not already) by going to your account in
# the top right corner > My profile
API_KEY = ''

dashboard = meraki.DashboardAPI(API_KEY)

# Parameters
organization_id = 0000  # Enter your organization ID
network_id = ''
timespan = 3600  # The timespan is in second

avg_signal_s = 0  # Average signal strength
count = 0
total_signal = 0


clients = dashboard.networks.getNetworkClients(network_id, total_pages=300, timespan=timespan)

# Signal Strength history per clients for the last 3600 seconds
for x in clients:

    # Retrieves only wireless clients
    if x['recentDeviceConnection'] == 'Wireless':

        user_signal_s = dashboard.wireless.getNetworkWirelessSignalQualityHistory(network_id, clientId=f'{x['id']}',
                                                                                  resolution=timespan,
                                                                                  timespan=timespan)

        # Retrieves only clients that reported their SNR values
        if user_signal_s[0]['snr'] is not None:
            count += 1  # Counts the number of entries

            # Convert the snr value to a string
            sg_to_compare = '', str(user_signal_s[0]['snr'])
            signal_value = ''
            for z in sg_to_compare:
                signal_value = signal_value + z

            # Additions the signal strength of all the users
            total_signal = (total_signal + int(signal_value))
            signal_value = ''  # Resets the signal strength value to an empty string


# Calculate the average signal strength of each user
avg_signal_s = total_signal / count

# Prints the average signal strength of all the clients for the last hour
print(f"The Average Signal Strength of wireless users for the last hour is {int(avg_signal_s)} dB")
