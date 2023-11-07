import xml.dom.minidom
import requests


from ncclient import manager
m = manager.connect(
    host="192.168.156.128",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    )

'''
print("#Supported Capabilities (YANG models):")
for capability in m.server_capabilities:
    print(capability)
'''

# netconf_reply = m.get_config(source="running")
# print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""
netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

#Change hostname to SETeamsCSR1000v
netconf_hostname = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>SETeamsCSR1000v</hostname>
    </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

#Create interface Loopback3
netconf_loopback = """
<config>
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
<interface>
<Loopback>
<name>3</name>
<description>My first NETCONF loopback</description>
<ip>
<address>
<primary>
<address>10.3.3.3</address>
<mask>255.255.255.0</mask>
</primary>
</address>
</ip>
</Loopback>
</interface>
</native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_loopback)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Enable syslog monitoring (severity level: warning)
netconf_syslog = """
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running/>
    </target>
    <config>
      <syslog xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-syslog">
        <console xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-syslog">
          <severity>warning</severity>
        </console>
        <monitor xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-syslog">
          <severity>warning</severity>
        </monitor>
        <file xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-syslog">
          <severity>
        </file>
      </syslog>
    </config>
  </edit-config>
</rpc>
"""

# Copy the running-config to startup-config
netconf_copyrunstart = """
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <copy-config>
    <target>
      <startup/>
    </target>
    <source>
      <running/>
    </source>
  </copy-config>
</rpc>
"""

# Push successful NETCONF message to Webex room
access_token = '' # <-- Place your API access token here
room_id = '' # <-- Place your Webex room ID here
message = 'NETCONF: **running-config** pushed and saved!'
url = 'https://webexapis.com/v1/messages'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'roomId': room_id, 'markdown': message}
res = requests.post(url, headers=headers, json=params)
print(res.json())
