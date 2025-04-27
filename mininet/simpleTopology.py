from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.node import RemoteController

class SimpleTopology(Topo):
    "Simple topology with one switch and two hosts."

    def build(self):
        # Add switch
        switch = self.addSwitch("s1")

        # Add hosts
        host1 = self.addHost("h1", ip="10.0.0.1/24")
        host2 = self.addHost("h2", ip="10.0.0.2/24")

        # Connect hosts to the switch
        self.addLink(host1, switch)
        self.addLink(host2, switch)

def run():
    "Create and run the Mininet network."
    topo = SimpleTopology()
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip="ryu-mininet", port=6653))

    net.start()
    print("Network started. Use 'pingall' to test connectivity.")
    
    # Open CLI for manual commands
    CLI(net)

    # Stop the network when done
    net.stop()

if __name__ == "__main__":
    setLogLevel("info")
    run()