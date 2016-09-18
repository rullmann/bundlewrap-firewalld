# bundlewrap-firewalld

`bundlewrap-firewalld` installs firewalld. It provides an action to reload firewalld after changes to other bundles.
Additionally it's possible to open custom ports.

## Compatibility

This bundle has been tested on the following systems:

| OS          | `[x]` |
| ----------- | ----- |
| CentOS 7    | `[x]` |
| Fedora 24   | `[x]` |
| RHEL 7      | `[ ]` |
| Fedberry 23 | `[ ]` |

## Requirements

(!) Make sure you have access to a remote console in case firewalld denies your access to the system.

## Metadata

    'metadata': {
        'firewalld': { #optional
            'ports': [
                "321/tcp",
                "456/udp",
            ],
        },
    }
