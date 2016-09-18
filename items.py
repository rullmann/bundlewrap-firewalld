pkg_yum = {
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
        'enabled': True,
        'needs': [
            "pkg_yum:firewalld",
        ],
    },
}

default_zone = node.metadata.get('firewalld', {}).get('default_zone')
if node.metadata.get('firewalld', {}).get('default_zone'):
    for interface in node.metadata['interfaces']:
        actions['firewalld_set_default_zone_{}'.format(interface)] = {
            'command': "firewall-cmd --permanent --zone={} --add-interface={}".format(default_zone, interface),
            'unless': "firewall-cmd --list-interfaces --zone={} | grep {}".format(default_zone, interface),
            'cascade_skip': False,
            'needs': [
                "pkg_yum:firewalld",
            ],
            'triggers': [
                "action:firewalld_reload",
            ],
        }

for port in node.metadata.get('firewalld', {}).get('ports', {}):
    actions['firewalld_add_port_{}'.format(port)] = {
        'command': "firewall-cmd --permanent --add-port={}".format(port),
        'unless': "firewall-cmd --list-ports | grep {}".format(port),
        'cascade_skip': False,
        'needs': [
            "pkg_yum:firewalld",
        ],
        'triggers': [
            "action:firewalld_reload",
        ],
    }
