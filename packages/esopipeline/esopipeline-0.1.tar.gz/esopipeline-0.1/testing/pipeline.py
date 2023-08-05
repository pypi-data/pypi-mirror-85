#! /usr/bin/env python3

import esofits
import esorex

def create_gravity():
    ins = 'gravity'
    recipes = ['dark', 'p2vm', 'vis', 'viscal']
    nconf = esorex.create_config_files(ins, recipes)
    return nconf

if __name__ == "__main__":
    try:
        nconf = create_gravity()
        print('created {} config file(s)'.format(nconf))
        nconf = create_gravity()
        print('created {} config file(s)'.format(nconf))
    except Exception as e:
        # print('error:', e)
        raise e
