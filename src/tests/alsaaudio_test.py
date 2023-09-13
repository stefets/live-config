#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import alsaaudio

def main(args=None):
	print(alsaaudio.pcms())
	print("------------------------------------------")
	print(alsaaudio.cards())
	print("------------------------------------------")
	card_info = {}
	for device_number, card_name in enumerate(alsaaudio.cards()):
		card_info[card_name] = "hw:%s,0" % device_number
		print(card_info[card_name])
	


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
