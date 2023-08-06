import sys
import argparse
from .megafon import main

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog="pymegafon", description='MegaFon Account Library')
	parser.add_argument("--login", "-l", dest="login", metavar="login", required=False, type=str, help="Account login (ex. +79990001234)")
	parser.add_argument("--password", "-p", dest="password", metavar="password", required=False, type=str, help="Account password")
	parser.add_argument("--check-balance", "-B", dest="command", required=False, action='store_const', const="do_check_balance", help="Check balance")
	parser.add_argument("--check-remainings", "-R", dest="command", required=False, action='store_const', const="do_check_remainings", help="Check subscription remainings")
	parser.add_argument("--list-subscriptions", "-L", dest="command", required=False, action='store_const', const="do_list_subscriptions", help="List subscriptions")
	parser.add_argument("--debug", "-d", dest="debug", required=False, default=False, action='store_true', help="Enable debug")
	
	args = parser.parse_args(sys.argv[1:])
	main(login=args.login, password=args.password, command=args.command, debug=args.debug)
