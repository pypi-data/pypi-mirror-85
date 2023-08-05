from mininet.log import setLogLevel, info, debug
from ipmininet.cli import IPCLI

from terranet.topo import HybridBackupTerragraphTopo
from terranet.net import Terranet
from terranet.controller import RyuManager


if __name__ == '__main__':
    setLogLevel('info')
    topo = HybridBackupTerragraphTopo()
    net = Terranet(topo=topo)
    module_path = 'terranet.ryu.app'
    apps = ('customer_flow_pipeline',
            'customer_stats_monitor')
    modules = [ '.'.join([module_path, x]) for x in apps ]
    ryu_manager = RyuManager('ryu-manager', modules=modules)
    net.addController(ryu_manager)
    net.start()
    IPCLI(net)
    net.stop()
