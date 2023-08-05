import os
import requests
import json

class SlackNotify:
  def __init__(self, bot_oauth_token, user_oauth_token, 
      post_message_url='https://slack.com/api/chat.postMessage',
      search_message_url='https://slack.com/api/search.messages',
      reaction_url='https://slack.com/api/reactions.add',
      reaction_remove_url='https://slack.com/api/reactions.remove',
      update_message_url='https://slack.com/api/chat.update'
     ):

     self.BOT_OAUTH_TOKEN = bot_oauth_token
     self.OAUTH_TOKEN = user_oauth_token
     self.POST_MESSAGE_URL = post_message_url
     self.SEARCH_MESSAGE_URL = search_message_url
     self.REACTION_URL = reaction_url
     self.REACTION_REMOVE_URL = reaction_remove_url
     self.UPDATE_URL = update_message_url

  def post_message(self, channel_id, message, thread_ts=None, emoji=None):
    payload = {
      "channel": channel_id,
      "text": message
    }

    if thread_ts:
      payload['thread_ts'] = thread_ts

    headers = {
      "Authorization": "Bearer " + self.BOT_OAUTH_TOKEN,
      "Content-type": "application/json;charset=UTF-8"
    }
    
    resp = requests.post(self.POST_MESSAGE_URL, json=payload, headers=headers)

    # TODO: Need to check response status code
    resp_json = json.loads(resp.text)

    if emoji:
      self.reaction(channel_id, emoji, resp_json['ts'])
    
    return resp_json

  def find_messages(self, channel_id, text):
    payload = {
      "channel": channel_id
    }

    params = {
      "query": "\"" + text + "\"",
      "sort": "timestamp",
      "sort_dir": "desc"
    }

    headers = {
      "Authorization": "Bearer " + self.OAUTH_TOKEN,
      "Content-type": "application/json;charset=UTF-8"
    }
    
    resp = requests.get(self.SEARCH_MESSAGE_URL, params=params, json=payload, headers=headers)

    # TODO: Need to check response status code
    resp_json = json.loads(resp.text)
    return resp_json

  def reaction(self, channel_id, emoji, ts):
    payload = {
      "channel": channel_id,
      "timestamp": ts,
      "name": emoji
    }

    headers = {
      "Authorization": "Bearer " + self.BOT_OAUTH_TOKEN,
      "Content-type": "application/json;charset=UTF-8"
    }
    
    resp = requests.post(self.REACTION_URL, json=payload, headers=headers)
    
    # TODO: Need to check response status code
    resp_json = json.loads(resp.text)
    return resp_json

  def remove_reaction(self, channel_id, emoji, ts):
    payload = {
      "channel": channel_id,
      "timestamp": ts,
      "name": emoji
    }

    headers = {
      "Authorization": "Bearer " + self.BOT_OAUTH_TOKEN,
      "Content-type": "application/json;charset=UTF-8"
    }
    
    resp = requests.post(self.REACTION_REMOVE_URL, json=payload, headers=headers)

    # TODO: Need to check response status code
    resp_json = json.loads(resp.text)
    return resp_json

  def edit_message(self, channel_id, message, ts, emoji):
    payload = {
      "channel": channel_id,
      "ts": ts,
      "text": message
    }

    headers = {
      "Authorization": "Bearer " + self.BOT_OAUTH_TOKEN,
      "Content-type": "application/json;charset=UTF-8"
    }
    
    resp = requests.post(self.UPDATE_URL, json=payload, headers=headers)

    # TODO: Need to check response status code
    if emoji:
      self.reaction(channel_id, emoji, ts)
    
    resp_json = json.loads(resp.text)
    return resp_json

# post_message(CHANNEL_ID, "Test a message", None, 'call_me_hand')
# reaction(CHANNEL_ID, 'tada', '1605086375.000900')
# find_messages(CHANNEL_ID, "Test a message")
# post_message(CHANNEL_ID, "Reply to message", '1605086946.001900', 'tada')
# edit_message(CHANNEL_ID, "Reply to message. This message has been edited", '1605089273.002500', 'call_me_hand')
# remove_reaction(CHANNEL_ID, 'call_me_hand', '1605089273.002500')