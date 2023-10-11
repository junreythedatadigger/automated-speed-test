import os
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Credential file path
absolute_path = os.path.dirname(__file__)                               # the current location of this project
relative_path = "data-analyst-project-01-384107-9457afc61153.json"      # relative path credential
full_path = os.path.join(absolute_path, relative_path)                  # full path of credential

print(full_path)

# Google Sheets Settings
spreadsheet_id = "139-CU26KtY9eJ6H8Vm8Ygp89l7d7q9M7_GjrJ0noBZU"
credentials_file = full_path

# Connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key(spreadsheet_id).sheet1

# index = 2

print(f'{sheet.row_count}')
print(len(sheet.col_values(1)))

# Get the last column with values then add 1
index = len(sheet.col_values(1)) + 1

while True:
#     # sheet.update_acell('A'+ str(index),index) # Working
    

    cell_rows = sheet.range('A'+str(index)+':H'+str(index))

    print(cell_rows)

    for cell in cell_rows:
        cell.value = index

    sheet.update_cells(cell_rows)

    time.sleep(5)
    index += 1


# # Select a range
# cell_list = worksheet.range('A1:C7')

# for cell in cell_list:
#     cell.value = 'O_o'

# # Update in batch
# worksheet.update_cells(cell_list)


# #################################################################################

# import paho.mqtt.client as mqtt
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # MQTT Settings
# mqtt_broker_address = "mqtt broker address"
# mqtt_topic = "your mqtt topic"

# # Google Sheets Settings
# spreadsheet_id = "your google sheet id"
# credentials_file = "path to your service account JSON file"

# # Connect to Google Sheets
# scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
# client = gspread.authorize(credentials)
# sheet = client.open_by_key(spreadsheet_id).sheet1

# # MQTT Callbacks
# def on_message(client, userdata, message):
#     payload = message.payload.decode("utf-8")
#     # Process and update the Google Sheet with the received payload
#     sheet.append_row([payload])

# # MQTT Client Setup
# client = mqtt.Client()
# client.on_message = on_message
# client.connect(mqtt_broker_address, 1883, 60)
# client.subscribe(mqtt_topic)

# # Start MQTT Loop
# client.loop_forever()
