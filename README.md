# cryptocurrency-bot

Cryptocurrency donation tracking bot for mattermost

A hacked together python script for tracking cryptocurrency donations. 
Currently only works for bitcoin, using the blockchain.info JSON API.

Generally untested, use with caution.

It will post the latest donations to Mattermost via Incoming Webhooks.

It should run periodically, probably through a cronjob or something similar.
