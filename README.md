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
            'ports': [ # optional, add custom ports which will be opened
                "321/tcp",
                "456/udp",
            ],
        },
        'interfaces': { # required, to set a default-zone and for other actions
            'eth0': {
                'ip_address': '172.16.16.42',
            },
            'tun0': {
                'ip_address': '10.10.10.42',
            },
        },
    }
