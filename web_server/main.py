from web_server import *
import sys, getopt
import logging

def main(argv):
    try: 
        ip = ''
        try:
          opts, args = getopt.getopt(argv,"hi:c:i:")
        except getopt.GetoptError as e:
          print (e)
          print ('test.py -i <outgoing IP>')
          sys.exit(2)
        for opt, arg in opts:
          if opt == '-h':
             print ('test.py -i <outgoing IP>')
             sys.exit()
          elif opt in ("-c"):
             conf_file = arg
          elif opt in ("-i"):
             ip = arg

        web_server = AudioHubWebServer(ip, conf_file)
        web_server.start()

    except KeyboardInterrupt:
        web_server.stop()
    except Exception as e:
        logging.exception("Exception occurred")

if __name__ == "__main__":
   main(sys.argv[1:])