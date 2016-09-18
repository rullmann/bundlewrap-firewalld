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
