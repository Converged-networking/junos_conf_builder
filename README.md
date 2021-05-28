# junos_conf_builder

**junos_conf_builder** is a role that generates Junos OS configuration from parameters native to ansible. The data model used as input is based on the output of `show configuration | display json`, when converted to YAML this is the exact input for this model.

This role focuses on generating the valid syntax for Junos OS devices to be able to parse it. In no way does it check if the configuration as a whole is valid, garbage in is garbage out.

I believe JUNOS devices have different syntaxes so at least for now the templates are based on the following models:

- EX2300

## Requirements

- Python >= 3.8
- ansible >= 4.0.0
- selinux (If selinux is enabled)

## Role Variables

The following default variables are set to configure the output directory:

### Default vars

#### root_dir

**root_dir** is set to inventory_dir which is set by ansible to the directory where the inventory file is located

#### config_dir_name

**config_dir_name** is the directory name in which the generated configs will be placed and defaults to **configs**

#### config_dir

**config_dir** is the directory in which **config_dir_name** will be placed, this is set to the **root_dir** by default

### Parameters

#### configuration

**configuration** contains the configuration for the Junops JUNOS device and should be provided.

## Example Playbook

```yaml
---
- hosts: localhost
  connection: local
  gather_facts: false

  vars:
    inventory_dir: .
    configuration:
      system:
        login:
          user:
            - name: admin
              full-name: admin
              uid: 2000
              class: super-user
              authentication:
                encrypted-password: $5$ac606172c5011f97569a0b7960ae344e7d76d7b93eee312839b44694ccebcadd
          message: "test message"
        root-authentication:
          encrypted-password: $5$ac606172c5011f97569a0b7960ae344e7d76d7b93eee312839b44694ccebcadd
        services:
          ssh:
            root-login: deny
          netconf:
            ssh:
              port: 830
        host-name: test1
        time-zone: Europe/Amsterdam
        name-server:
          - name: 10.0.0.1
          - name: 10.0.0.2
      chassis:
        redundancy:
          graceful-switchover:
        aggregated-devices:
          ethernet:
            device-count: 2
      interfaces:
        interface-range:
          - name: uplink-range
            member:
              - name: xe-0/1/0
              - name: xe-1/1/0
            description: Uplink
            ether-options:
              ieee-802.3ad:
                bundle: ae0
          - name: office-range
            member:
              - name: ge-1/0/1
              - name: ge-1/0/2
            memberrange:
              - name: ge-1/0/4
                end-range: ge-1/0/19
              - name: ge-0/0/2
                end-range: ge-0/0/30
            description: "Access: Office"
            unit:
              - name: 0
                family:
                  ethernet-switching:
                    interface-mode: access
        interface:
          - name: ae0
            description: Uplink
            aggregated-ether-options:
              minimum-links: 1
              lacp:
                active:
                  - null
            unit:
              - name: 0
                family:
                  ethernet-switching:
                    interface-mode: trunk
                    vlan:
                      members:
                        - vl_101
                        - vl_130
          - name: irb
            unit:
              - name: 130
                family:
                  inet:
                    address:
                      - name: 1.1.1.1/24
      forwarding-options:
        storm-control-profiles:
          - name: default
            all:
      policy-options:
        prefix-list:
          - name: mgmt-prefixes
            prefix-list-item:
              - name: 1.2.0.0/24
              - name: 1.2.1.0/24
          - name: ntp-servers
            apply-path: "system ntp server <*>"
          - name: snmp-servers
            apply-path: "snmp community <*> clients <*>"
          - name: localhost
            prefix-list-item:
              - name: 127.0.0.1/32
          - name: radius-servers
            apply-path: "access radius-server <*>"
      routing-options:
        nonstop-routing:
        static:
          route:
            - name: 0.0.0.0/0
              next-hop:
                - 10.0.0.1
      protocols:
        igmp-snooping:
          vlan:
            - name: default
        rstp:
          interface:
            - name: all
      vlans:
        vlan:
          - name: default
            vlan-id: 1
            l3-interface: irb.0
  roles:
    - junos_conf_builder
```

## License

[BSD](https://github.com/Converged-networking/junos_conf_builder/blob/main/LICENSE)

## Author Information

Marvin Kuurstra

github: Converged-networking
