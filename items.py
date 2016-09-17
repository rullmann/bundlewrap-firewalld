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
