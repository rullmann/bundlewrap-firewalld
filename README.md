# bundlewrap-firewalld

`bundlewrap-firewalld` installs firewalld. It provides an action to reload firewalld after changes to other bundles.
Additionally it's possible to open custom ports.

## Compatibility

This bundle has been tested on the following systems:

| OS          | `[x]` |
| ----------- | ----- |
| Fedora 24   | `[x]` |
| Fedberry 23 | `[ ]` |

## Requirements

(!) Make sure you have access to a remote console in case firewalld denies your access to the system.

## Metadata

    'metadata': {
        'firewalld': { 
            'default_zone': 'public', # optional, add all interfaces to this zone
            'custom_zones': True, # optional, add each interface to the specified zone
            'ports': [ # optional, add custom ports which will be opened
                "321/tcp",
                "456/udp",
            ],
        },
        'interfaces': { # required, to set a default-zone and for other actions
            'eth0': {
                'ip_address': '172.16.16.42',
                'firewalld_zone': 'public', # required if `custom_zones` is set to True.
            },
            'tun0': {
                'ip_address': '10.10.10.42',
                'firewalld_zone': 'internal', # required if `custom_zones` is set to True.
            },
        },
    }

### Example Metdata

#### Set a default interface for all interfaces

    'metadata': {
        'firewalld': { 
            'default_zone': 'internal',
        },
        'interfaces': {
            'eth0': {},
            'tun0': {},
        },
    }

#### Set custom zones for each interface

    'metadata': {
        'firewalld': { 
            'custom_zones': True,
        },
        'interfaces': {
            'eth0': {
                'firewalld_zone': 'public',
            },
            'tun0': {
                'firewalld_zone': 'internal',
            },
        },
    }

## Notes

Changing the zone of an interface will always end up with an error from bw, e.g.:

    ✘ bw-test-fedora  firewalld  action:firewalld_set_custom_zone_ens37 failed

`firewaldd_cmd` displays a warning when setting up the zone and therefores exits with status 254 instead of 0:

    ┌ root@bw-test-fedora /root
    └ # firewall-cmd --permanent --zone=public --add-interface=ens37
    The interface is under control of NetworkManager, setting zone to 'public'.
    ┌ root@bw-test-fedora /root
    └ # echo $status
    254

A second run of `bq apply` will show that the zone has been set correctly.
In case you want to check manually just run `firewall-cmd --list-interfaces --zone=<zone>`