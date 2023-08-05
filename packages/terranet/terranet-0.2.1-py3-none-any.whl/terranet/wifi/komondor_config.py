import os
import itertools
import collections
from configparser import ConfigParser

from .channel import Channel


def _read_komondor_files(directory, cls):
    config_dict = collections.OrderedDict()
    files = [f for f in sorted(os.listdir(directory)) if f.endswith(".cfg")]
    for cfg_file in files:
        path = os.path.join(directory, cfg_file)
        cfg = cls(path)
        config_dict[cfg_file] = cfg
    return config_dict


def read_komondor_configs(dir):
    return _read_komondor_files(dir, KomondorConfig)


def read_komondor_results(dir):
    return _read_komondor_files(dir, KomondorResult)


class KomondorBaseConfig(ConfigParser):
    def __init__(self,
                 cfg_file=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.cfg_file = cfg_file
        if self.cfg_file:
            self.read(cfg_file)

    # Keep case for options https://stackoverflow.com/a/23007845
    def optionxform(self, optionstr):
        return optionstr

    def sections_by_value(self, key, value):
        return [self[x] for x in self.sections() if self[x].get(key) == value]

    def nodes(self):
        return [self[x] for x in self.sections() if not x == 'System']


class KomondorConfig(KomondorBaseConfig):
    def __init__(self, cfg_file=None):
        super(KomondorConfig, self).__init__(cfg_file=cfg_file)

    def system(self):
        return self["System"]

    def access_points(self):
        return self.sections_by_value("type", "0")

    def stations(self):
        return self.sections_by_value("type", "1")

    def nodes_by_wlan_code(self, wlan_code):
        return self.sections_by_value("wlan_code", wlan_code)

    def get_stations_by_access_point(self, ap):
        return list(filter(lambda x: x["type"] == "1",
                           self.nodes_by_wlan_code(ap["wlan_code"])))

    def wifi5_links_for_access_point(self, ap):
        return [(ap.name, sta.name)
                for sta in self.get_stations_by_access_point(ap)]

    def wifi5GHz_links(self):
        return reduce(lambda x, y: x + self.wifi5_links_for_access_point(y),
                      self.access_points(), [])

    def wifi60GHz_links(self):
        aps = map(lambda x: x.name,
                  self.sort_west_to_east(self.access_points()))
        return [(aps[i], aps[i+1]) for i, _ in enumerate(aps)
                if i+1 < len(aps)]

    def sort_west_to_east(self, nodes):
        return sorted(nodes, key=lambda x: x["x"])

    def ap_channel_configurations(self):
        channel_config = []
        for ap in self.access_points():
            wlan_code = ap['wlan_code']
            min_channel_allowed = ap['min_channel_allowed']
            max_channel_allowed = ap['max_channel_allowed']
            ch = Channel.channel_num(min_channel_allowed, max_channel_allowed)
            channel_config.append({'name': ap.name,
                                   'wlan_code': wlan_code,
                                   'channel': ch,
                                   'min_channel_allowed': min_channel_allowed,
                                   'max_channel_allowed': max_channel_allowed})
        return channel_config



class KomondorConfigSection(collections.OrderedDict):
    def __init__(self, name, *args, **kwargs):
        self.name = name
        super().__init__(*args, **kwargs)


class KomondorSystemConfig(KomondorConfigSection):
    def __init__(self, *args, **kwargs):
        name = "System"
        defaults = collections.OrderedDict([
            ("num_channels", 50),
            ("basic_channel_bandwidth", 20),
            ("pdf_backoff", 0),
            ("pdf_tx_time", 1),
            ("packet_length", 12000),
            ("num_packets_aggregated", 64),
            ("path_loss_model_default", 5),
            ("path_loss_model_indoor_indoor", 5),
            ("path_loss_model_indoor_outdoor", 8),
            ("path_loss_model_outdoor_outdoor", 7),
            ("capture_effect", 20),
            ("noise_level", -95),
            ("adjacent_channel_model", 0),
            ("collisions_model", 0),
            ("constant_PER", 0),
            ("traffic_model", 99),
            ("backoff_type", 0),
            ("cw_adaptation", 1),
            ("pifs_activated", 0),
            ("capture_effect_model", 1)])
        config = defaults
        config.update(kwargs)
        super().__init__(name, *args, **config)


class KomondorNodeConfig(KomondorConfigSection):
    def __init__(self, name, *args, **kwargs):
        defaults = collections.OrderedDict([
            ("type", 0),
            ("wlan_code", "A"),
            ("destination_id", -1),
            ("x", 0),
            ("y", 0),
            ("z", 0),
            ("primary_channel", 0),
            ("min_channel_allowed", 0),
            ("max_channel_allowed", 0),
            ("cw", 16),
            ("cw_stage", 5),
            ("tpc_min", 30),
            ("tpc_default", 30),
            ("tpc_max", 30),
            ("cca_min", -82),
            ("cca_default", -82),
            ("cca_max", -82),
            ("tx_antenna_gain", 0),
            ("rx_antenna_gain", 0),
            ("channel_bonding_model", 1),
            ("modulation_default", 0),
            ("central_freq", 5),
            ("lambda", 10000),
            ("ieee_protocol", 1),
            ("traffic_load", 1000),
            ("node_env", "outdoor")])
        config = defaults
        config.update(kwargs)
        if config["type"] == 0:
            name = "Node_AP_{}".format(name)
        else:
            name = "Node_STA_{}".format(name)
        super().__init__(name, *args, **config)


class KomondorResult(KomondorBaseConfig):
    def __init__(self, cfg_file=None):
        super().__init__(cfg_file=cfg_file)

    def nodes_by_wlan(self, wlan):
        return self.sections_by_value('wlan', wlan)

    def total_throughput(self):
        return sum([int(self[x]['throughput']) for x in self.sections()])

    def wlan_throughput(self, wlan):
        return sum([int(x['throughput']) for x in self.nodes_by_wlan(wlan)])

    def wlans(self):
        return list(sorted(set([self[x]['wlan'] for x in self.sections()])))
