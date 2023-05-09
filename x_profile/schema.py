INBOUND_SETTINGS = '''
{
  "clients": [
    {
      "id": "{uuid}",
      "flow": "xtls-rprx-vision",
      "email": "",
      "limitIp": 0,
      "totalGB": 10737418240,
      "expiryTime": {expiry_time},
      "enable": true,
      "tgId": "{tag}",
      "subId": ""
    }
  ],
  "decryption": "none",
  "fallbacks": []
}
'''

STREAM_SETTINGS = '''
{
  "network": "tcp",
  "security": "reality",
  "realitySettings": {
    "show": false,
    "xver": 0,
    "dest": "discord.com:443",
    "serverNames": [
      "www.discord.com"
    ],
    "privateKey": "kOZBGRo4jyn2xUFFlvguDfoXWXhaHdV433FHWNgs8Hc",
    "minClient": "",
    "maxClient": "",
    "maxTimediff": 0,
    "shortIds": [
      "3067e603"
    ],
    "settings": {
      "publicKey": "iv-KCArDYXw99cIybEnUAzZhJyufRTm8wkLeH6eIiyo",
      "fingerprint": "firefox",
      "serverName": ""
    }
  },
  "tcpSettings": {
    "acceptProxyProtocol": false,
    "header": {
      "type": "none"
    }
  }
}
'''

SNIFFING_SETTINGS = '''
{
  "enabled": true,
  "destOverride": [
    "http",
    "tls",
    "quic"
  ]
}
'''
