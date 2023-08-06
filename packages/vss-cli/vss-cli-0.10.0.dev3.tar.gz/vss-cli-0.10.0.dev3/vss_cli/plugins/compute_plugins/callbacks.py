"""Compute Callback module for VSS CLI (vss-cli)."""
from click.exceptions import BadParameter

from vss_cli.autocompletion import _init_ctx
from vss_cli.config import Configuration
from vss_cli.helper import to_tuples


def process_networks_opt(ctx: Configuration, param, value):
    """Process network option."""
    _init_ctx(ctx)
    if value is not None:
        networks = list()
        for nic in value:
            _nic = to_tuples(nic)[0]
            _network = _nic[0]
            if len(_nic) > 1:
                _type = ctx.client.get_vm_nic_type_by_name(_nic[1])
                _type = _type[0]['type']
            else:
                _type = 'vmxnet3'
            _net = ctx.client.get_network_by_name_or_moref(_network)
            networks.append({'network': _net[0]['moref'], 'type': _type})
        return networks


def process_scsi_opt(ctx: Configuration, param, value):
    """Process SCSI spec option."""
    _init_ctx(ctx)
    if value is not None:
        devices = list()
        for dev in value:
            _dev = to_tuples(dev)[0]
            _type = _dev[0]
            if len(_dev) > 1:
                _sharing = ctx.client.get_vm_scsi_sharing_by_name(_dev[1])
                _sharing = _sharing[0]['type']
            else:
                _sharing = 'nosharing'
            _t = ctx.client.get_vm_scsi_type_by_name(_type)
            devices.append({'type': _t[0]['type'], 'sharing': _sharing})
        return devices


def process_disk_opt(ctx: Configuration, param, value):
    """Process Disk spec option.

    <capacity>=<backing_mode>=<backing_sharing>
    """
    _init_ctx(ctx)
    if value is not None:
        devices = list()
        _backing_mode = 'persistent'
        _sharing_mode = 'sharingnone'
        for dev in value:
            _dev = to_tuples(dev)[0]
            try:
                _capacity = int(_dev[0])
            except ValueError:
                raise BadParameter('capacity must be a number')
            # backing
            if len(_dev) > 1:
                _spec = to_tuples(_dev[1])[0]
                if len(_spec) > 0:
                    _backing_mode = ctx.client.get_vm_disk_backing_mode_by_name(  # NOQA:
                        _spec[0]
                    )
                    _backing_mode = _backing_mode[0]['type']
                if len(_spec) > 1:
                    _sharing_mode = ctx.client.get_vm_disk_backing_sharing_by_name(  # NOQA
                        _spec[1]
                    )
                    _sharing_mode = _sharing_mode[0]['type']
            devices.append(
                {
                    'capacity_gb': _capacity,
                    'backing_mode': _backing_mode,
                    "backing_sharing": _sharing_mode,
                }
            )
        return devices
