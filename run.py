# -*- coding: utf-8 -*-
import os
import spidder
import configparser

if __name__ == '__main__':
    cur_path=os.path.dirname(os.path.realpath(__file__))
    account_path=os.path.join(cur_path,'account.conf')
    config=configparser.ConfigParser(allow_no_value=True)
    config.read(account_path)
    accounts = config.items("account")
    for item in accounts:
        s = spidder.Spidder(item)
        s.start()

