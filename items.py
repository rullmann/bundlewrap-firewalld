pkg_dnf = {
    "firewalld": {},
}

actions = {
    'firewalld_reload': {
        'command': "firewall-cmd --reload",
        'triggered': True,
    },
}

svc_systemd = {
    'firewalld': {
        'needs': [
            "pkg_dnf:firewalld",
        ],
    },
}

files = {
    '/etc/firewalld/firewalld.conf': {
        'source': "firewalld.conf",
        'mode': "0644",
        'content_type': "mako",
        'needs': [
            "pkg_dnf:firewalld",
        ],
        'triggers': [
            "action:firewalld_reload",
        ],
    },
}

if node.metadata.get('firewalld', {}).get('default_zone'):
    default_zone = node.metadata.get('firewalld', {}).get('default_zone')
    for interface in node.metadata['interfaces']:
        actions['firewalld_set_default_zone_{}'.format(interface)] = {
            'command': "firewall-cmd --permanent --zone={} --add-interface={}".format(default_zone, interface),
            'unless': "firewall-cmd --list-interfaces --zone={} | grep {}".format(default_zone, interface),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
elif node.metadata.get('firewalld', {}).get('custom_zones', False):
    for interface in node.metadata['interfaces']:
        custom_zone = node.metadata.get('interfaces', {}).get(interface).get('firewalld_zone')
        actions['firewalld_set_custom_zone_{}'.format(interface)] = {
            'command': "firewall-cmd --permanent --zone={} --add-interface={}".format(custom_zone, interface),
            'unless': "firewall-cmd --list-interfaces --zone={} | grep {}".format(custom_zone, interface),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }

for port in node.metadata.get('firewalld', {}).get('ports', {}):
    if node.metadata.get('firewalld', {}).get('default_zone'):
        actions['firewalld_add_port_to_default_zone_{}'.format(port)] = {
            'command': "firewall-cmd --permanent --zone={} --add-port={}".format(default_zone, port),
            'unless': "firewall-cmd --zone={} --list-ports | grep {}".format(default_zone, port),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
    elif node.metadata.get('firewalld', {}).get('custom_zones', False):
        for interface in node.metadata['interfaces']:
            custom_zone = node.metadata.get('interfaces', {}).get(interface).get('firewalld_zone')
            actions['firewalld_add_port_{}_to_custom_zone_{}'.format(port, custom_zone)] = {
                'command': "firewall-cmd --permanent --zone={} --add-port={}".format(custom_zone, port),
                'unless': "firewall-cmd --zone={} --list-ports | grep {}".format(custom_zone, port),
                'cascade_skip': False,
                'needs': [
                    "pkg_dnf:firewalld",
                ],
                'triggers': [
                    "action:firewalld_reload",
                ],
            }
    else:
        actions['firewalld_add_port_{}'.format(port)] = {
            'command': "firewall-cmd --permanent --add-port={}".format(port),
            'unless': "firewall-cmd --list-ports | grep {}".format(port),
            'cascade_skip': False,
            'needs': [
                "pkg_dnf:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }
