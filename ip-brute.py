try:
	class bcolors:
	    HEADER = '\033[95m'
	    OKBLUE = '\033[94m'
	    OKCYAN = '\033[96m'
	    OKGREEN = '\033[92m'
	    WARNING = '\033[93m'
	    FAIL = '\033[91m'
	    ENDC = '\033[0m'
	    BOLD = '\033[1m'
	    UNDERLINE = '\033[4m'

	print(bcolors.OKCYAN + " ### ######        ######                                " + bcolors.ENDC)
	print("  #  #     #       #     # #####  #    # ##### ######    ")
	print("  #  #     #       #     # #    # #    #   #   #         ")
	print(bcolors.WARNING + "  #  ######  ##### ######  #    # #    #   #   #####     " + bcolors.ENDC)
	print("  #  #             #     # #####  #    #   #   #         ")
	print("  #  #             #     # #   #  #    #   #   #         ")
	print(bcolors.OKCYAN + " ### #             ######  #    #  ####    #   ######" + bcolors.ENDC)
	print(bcolors.UNDERLINE + "By " + bcolors.OKGREEN + "CCMD" + bcolors.ENDC + bcolors.ENDC + "\n")
	try:
	    import psutil
	except ImportError:
	    print("The 'psutil' library is not installed. Please install it by running:")
	    print(bcolors.FAIL + "pip install psutil" + bcolors.ENDC)
	    exit(1)

	import subprocess

	try:
		result = subprocess.run(['sudo', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except FileNotFoundError:
		print("sudo is not installed.\nInstall it by running 'apt-get install sudo'")
		exit(1)
	except subprocess.CalledProcessError:
		#Some error occurs so it's ignored.
		pass

	interfaces = psutil.net_if_addrs()

	import os
	mobile_data = os.popen('sudo settings get global mobile_data').read()
	print("Mobile Data: " + bcolors.OKGREEN + mobile_data + bcolors.ENDC + "\n")

	print("Choose carrier interface/current IP:")
	for i, (iface, addrs) in enumerate(interfaces.items()):
	    ip_addrs = [addr.address for addr in addrs if addr.family == 2]
	    if ip_addrs:
	        print(bcolors.BOLD + f"{i}. {iface}: {', '.join(ip_addrs)}" + bcolors.ENDC)
	    else:
	        print(f"{i}. {iface}: No IP")

	choice = int(input("\nSelect an interface(by number): "))
	try:
		selected_iface = list(interfaces.keys())[choice]
		selected_ip = list(interfaces.items())[choice][1][0][1]

		print(f"\n" + bcolors.OKCYAN + selected_iface + bcolors.ENDC + " selected")
		prefix = str(input("Enter prefix(e.g 10.202, 10.64): "))
		print("\nIf toggling occurs too quickly then modify the var")
		
		import itertools
		import time
		import threading
		import sys

		stop_event = threading.Event()
		def animate():
				for c in itertools.cycle(['|', '/', '-', '\\']):
					if stop_event.is_set():
						break
					sys.stdout.write("\r[" + bcolors.OKCYAN + "1"  + bcolors.ENDC + "] Performing enumeration for " + bcolors.UNDERLINE + bcolors.OKGREEN + selected_ip + bcolors.ENDC + bcolors.ENDC + " " + c)
					sys.stdout.flush()
					time.sleep(0.1)
				sys.stdout.write("\rFinished\n")
			

		t = threading.Thread(target=animate)

		verify_interface = psutil.net_if_addrs()
		verify_ip = list(verify_interface.items())[choice][1][0][1]
		started = False

		while True:
			if verify_ip.startswith(prefix):
				print("\n[" + bcolors.OKCYAN + "2" + bcolors.ENDC + "]" + " IP: " + bcolors.OKCYAN + verify_ip + bcolors.ENDC)
				if started:
					stop_event.set()
					sys.exit(0)
				break

			if not started:
				started = True
				t.start()
		
			if not verify_ip.startswith(prefix):
				subprocess.Popen('sudo cmd connectivity airplane-mode enable', shell=True)
				time.sleep(1.5)

				subprocess.Popen('sudo cmd connectivity airplane-mode disable', shell=True)
				time.sleep(5.5) #Modify based on network connectivity and strength

				verify_interface = psutil.net_if_addrs()
				verify_ip = list(verify_interface.items())[choice][1][0][1]


	except (IndexError, ValueError):
		print(bcolors.FAIL + "Select existing interface" + bcolors.ENDC)
except KeyboardInterrupt:
	if started:
		stop_event.set()
	print("Bye")