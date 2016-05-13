import Pyro4

from extract_scenes import ExtractScenes

if __name__ == '__main__':
    daemon = Pyro4.Daemon(host='172.17.0.4', port=7771)
    uri = daemon.register(ExtractScenes)
    print "proxy\n", uri
    daemon.requestLoop()
