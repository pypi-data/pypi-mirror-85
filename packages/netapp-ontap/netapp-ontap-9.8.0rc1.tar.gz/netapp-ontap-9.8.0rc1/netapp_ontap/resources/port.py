r"""
Copyright &copy; 2020 NetApp Inc.
All rights reserved.

## Overview
A port is a physical or virtual Ethernet network device. Physical ports may be combined into Link Aggregation Groups (LAGs or ifgrps), or divided into Virtual LANs (VLANs).<br/>
GET (collection), GET (instance), and PATCH APIs are available for all port types. POST and DELETE APIs are available for "lag" (ifgrp) and "vlan" port types.<br/>
## Retrieving network port information
The network ports GET API retrieves and displays relevant information pertaining to the ports configured in the cluster. The API retrieves the list of all ports configured in the cluster, or specifically requested ports. The fields returned in the response vary for different ports and configurations.
## Examples
### Retrieving all ports in the cluster
The following output displays the UUID, name, and port type for all ports configured in a 2-node cluster. The port types are physical, vlan, and lag (ifgrp).
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(list(Port.get_collection(fields="uuid,name,type")))

```
<div class="try_it_out">
<input id="example0_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example0_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example0_result" class="try_it_out_content">
```
[
    Port(
        {
            "uuid": "2d2c90c0-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d2c90c0-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "e0a",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "2d3004da-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d3004da-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "e0b",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "2d34a2cb-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d34a2cb-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "e0c",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "2d37189f-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/2d37189f-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "e0d",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "35de5d8b-f70d-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35de5d8b-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "name": "e0a",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "35de78cc-f70d-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35de78cc-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "name": "e0b",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "35dead3c-f70d-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35dead3c-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "name": "e0c",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "35deda90-f70d-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/35deda90-f70d-11e8-abdf-005056bb7fc8"
                }
            },
            "name": "e0d",
            "type": "physical",
        }
    ),
    Port(
        {
            "uuid": "42e25145-f97d-11e8-ade9-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/42e25145-f97d-11e8-ade9-005056bb7fc8"
                }
            },
            "name": "e0c-100",
            "type": "vlan",
        }
    ),
    Port(
        {
            "uuid": "569e0abd-f97d-11e8-ade9-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/569e0abd-f97d-11e8-ade9-005056bb7fc8"
                }
            },
            "name": "a0a",
            "type": "lag",
        }
    ),
]

```
</div>
</div>

---
### Retrieving a specific physical port
The following output displays the response when a specific physical port is requested. The system returns an error when there is no port with the requested UUID. Also, the "speed" field for the physical port is set only if the state of the port is up.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="2d37189f-f70d-11e8-b145-005056bb5b8e")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example1_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example1_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example1_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "Default",
        },
        "uuid": "2d37189f-f70d-11e8-b145-005056bb5b8e",
        "enabled": True,
        "speed": 1000,
        "mtu": 1500,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/2d37189f-f70d-11e8-b145-005056bb5b8e"
            }
        },
        "reachability": "not_repairable",
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "name": "Default",
            },
            {
                "ipspace": {"name": "Default"},
                "uuid": "df640ccf-72c4-11ea-b31d-005056bbfb29",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/df640ccf-72c4-11ea-b31d-005056bbfb29"
                    }
                },
                "name": "Default-1",
            },
        ],
        "name": "e0d",
        "type": "physical",
        "mac_address": "00:50:56:bb:62:2d",
        "state": "up",
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
        },
    }
)

```
</div>
</div>

---
### Retrieving a specific VLAN port
The following output displays the response when a specific VLAN port is requested. The system returns an error when there is no port with the requested UUID. Also, the "speed" field for a VLAN port is always set to zero if the state of the port is up. If the state of the port is down, the "speed" field is unset and not reported back.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="42e25145-f97d-11e8-ade9-005056bb7fc8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example2_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example2_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example2_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "Default",
        },
        "uuid": "42e25145-f97d-11e8-ade9-005056bb7fc8",
        "enabled": True,
        "speed": 0,
        "mtu": 1500,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/42e25145-f97d-11e8-ade9-005056bb7fc8"
            }
        },
        "reachability": "ok",
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "name": "Default",
            }
        ],
        "name": "e0e-100",
        "vlan": {
            "base_port": {
                "uuid": "35deff03-f70d-11e8-abdf-005056bb7fc8",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/35deff03-f70d-11e8-abdf-005056bb7fc8"
                    }
                },
                "name": "e0e",
                "node": {"name": "user-cluster-02"},
            },
            "tag": 100,
        },
        "type": "vlan",
        "mac_address": "00:50:56:bb:52:2f",
        "state": "up",
        "node": {
            "name": "user-cluster-02",
            "uuid": "6042cf47-f70c-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/6042cf47-f70c-11e8-abdf-005056bb7fc8"
                }
            },
        },
    }
)

```
</div>
</div>

---
### Retrieving a specific LAG port
The following output displays the response when a specific LAG port is requested. The system returns an error when there is no port with the requested UUID. The "lag.active_ports" field is set only if the state of the port is up. Also, the "speed" field for a LAG port is always set to zero if the state of the port is up. If the state of the port is down, the "speed" field is unset and not reported back.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="569e0abd-f97d-11e8-ade9-005056bb7fc8")
    resource.get(fields="*")
    print(resource)

```
<div class="try_it_out">
<input id="example3_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example3_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example3_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "Default",
        },
        "uuid": "569e0abd-f97d-11e8-ade9-005056bb7fc8",
        "lag": {
            "mode": "singlemode",
            "active_ports": [
                {
                    "uuid": "35df318d-f70d-11e8-abdf-005056bb7fc8",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df318d-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "name": "e0f",
                }
            ],
            "member_ports": [
                {
                    "uuid": "35df318d-f70d-11e8-abdf-005056bb7fc8",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df318d-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "name": "e0f",
                    "node": {"name": "user-cluster-02"},
                },
                {
                    "uuid": "35df5bad-f70d-11e8-abdf-005056bb7fc8",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df5bad-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "name": "e0g",
                    "node": {"name": "user-cluster-02"},
                },
                {
                    "uuid": "35df9926-f70d-11e8-abdf-005056bb7fc8",
                    "_links": {
                        "self": {
                            "href": "/api/network/ethernet/ports/35df9926-f70d-11e8-abdf-005056bb7fc8"
                        }
                    },
                    "name": "e0h",
                    "node": {"name": "user-cluster-02"},
                },
            ],
            "distribution_policy": "mac",
        },
        "enabled": True,
        "speed": 0,
        "mtu": 1500,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/569e0abd-f97d-11e8-ade9-005056bb7fc8"
            }
        },
        "reachability": "repairable",
        "reachable_broadcast_domains": [
            {
                "ipspace": {"name": "Default"},
                "uuid": "c7934b4f-691f-11ea-87fd-005056bb1ad3",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/broadcast-domains/c7934b4f-691f-11ea-87fd-005056bb1ad3"
                    }
                },
                "name": "Default",
            }
        ],
        "name": "a0a",
        "type": "lag",
        "mac_address": "02:50:56:bb:7f:c8",
        "state": "up",
        "node": {
            "name": "user-cluster-02",
            "uuid": "6042cf47-f70c-11e8-abdf-005056bb7fc8",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/6042cf47-f70c-11e8-abdf-005056bb7fc8"
                }
            },
        },
    }
)

```
</div>
</div>

---
### Retrieving all LAG (ifgrp) ports in the cluster
This command retrieves all LAG ports in the cluster (that is, all ports with type=LAG). The example shows how to filter a GET collection based on type.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    print(
        list(
            Port.get_collection(
                type="lag",
                fields="name,enabled,speed,mtu",
                **{"node.name": "user-cluster-01"}
            )
        )
    )

```
<div class="try_it_out">
<input id="example4_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example4_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example4_result" class="try_it_out_content">
```
[
    Port(
        {
            "uuid": "0c226db0-4b63-11e9-8113-005056bbe040",
            "enabled": True,
            "speed": 0,
            "mtu": 1500,
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/0c226db0-4b63-11e9-8113-005056bbe040"
                }
            },
            "name": "a0b",
            "type": "lag",
            "node": {"name": "user-cluster-01"},
        }
    ),
    Port(
        {
            "uuid": "d3a84153-4b3f-11e9-a00d-005056bbe040",
            "enabled": True,
            "speed": 0,
            "mtu": 1500,
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/ports/d3a84153-4b3f-11e9-a00d-005056bbe040"
                }
            },
            "name": "a0a",
            "type": "lag",
            "node": {"name": "user-cluster-01"},
        }
    ),
]

```
</div>
</div>

---
## Creating VLAN and LAG ports
You can use the network ports POST API to create VLAN and LAG ports. If you supply the optional broadcast domain property, the specified broadcast domain will be assigned to the new port immediately.  Otherwise, within a few minutes automatic probing will determine the correct broadcast domain and will assign it to the port.  During that period of time, the port will not be capable of hosting interfaces.
<br/>
---
## Examples
### Creating a VLAN port
The following output displays the record returned after the creation of a VLAN port on "e0e" and VLAN tag "100".
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "vlan"
    resource.node.name = "user-cluster-01"
    resource.enabled = True
    resource.vlan.tag = 100
    resource.vlan.base_port.name = "e0e"
    resource.vlan.base_port.node.name = "user-cluster-01"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example5_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example5_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example5_result" class="try_it_out_content">
```
Port(
    {
        "uuid": "88b2f682-fa42-11e8-a6d7-005056bb5b8e",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/88b2f682-fa42-11e8-a6d7-005056bb5b8e"
            }
        },
        "vlan": {
            "base_port": {
                "uuid": "2d39df72-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/2d39df72-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "name": "e0e",
                "node": {"name": "user-cluster-01"},
            },
            "tag": 100,
        },
        "type": "vlan",
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
        },
    }
)

```
</div>
</div>

---
### Creating a VLAN port in a specific broadcast domain
The following output displays the record returned after the creation of a VLAN port on "e0e" and VLAN tag "100". Also, the VLAN port is added to the "Default" broadcast domain in the "Default" IPspace.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "vlan"
    resource.node.name = "user-cluster-01"
    resource.broadcast_domain.name = "Default"
    resource.broadcast_domain.ipspace.name = "Default    "
    resource.enabled = True
    resource.vlan.tag = 100
    resource.vlan.base_port.name = "e0e"
    resource.vlan.base_port.node.name = "user-cluster-01"
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example6_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example6_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example6_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/network/ethernet/broadcast-domains/36434bec-f70d-11e8-b145-005056bb5b8e"
                }
            },
            "name": "Default",
        },
        "uuid": "88b2f682-fa42-11e8-a6d7-005056bb5b8e",
        "enabled": True,
        "_links": {
            "self": {
                "href": "/api/network/ethernet/ports/88b2f682-fa42-11e8-a6d7-005056bb5b8e"
            }
        },
        "vlan": {
            "base_port": {
                "uuid": "2d39df72-f70d-11e8-b145-005056bb5b8e",
                "_links": {
                    "self": {
                        "href": "/api/network/ethernet/ports/2d39df72-f70d-11e8-b145-005056bb5b8e"
                    }
                },
                "name": "e0e",
                "node": {"name": "user-cluster-01"},
            },
            "tag": 100,
        },
        "type": "vlan",
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
            "_links": {
                "self": {
                    "href": "/api/cluster/nodes/faa56898-f70c-11e8-b145-005056bb5b8e"
                }
            },
        },
    }
)

```
</div>
</div>

---
### Creating a LAG (ifgrp) port
The following output displays the record returned after the creation of a LAG port with "e0f", "e0g" and "e0h" as member ports.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port()
    resource.type = "lag"
    resource.node.name = "user-cluster-01"
    resource.enabled = True
    resource.lag.mode = "singlemode"
    resource.lag.distribution_policy = "mac"
    resource.lag.member_ports = [
        {"name": "e0f", "node": {"name": "user-cluster-01"}},
        {"name": "e0g", "node": {"name": "user-cluster-01"}},
        {"name": "e0h", "node": {"name": "user-cluster-01"}},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example7_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example7_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example7_result" class="try_it_out_content">
```
Port(
    {
        "uuid": "1807772a-fa4d-11e8-a6d7-005056bb5b8e",
        "lag": {
            "mode": "singlemode",
            "member_ports": [
                {
                    "uuid": "2d3c9adc-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0f",
                    "node": {"name": "user-cluster-01"},
                },
                {
                    "uuid": "2d40b097-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0g",
                    "node": {"name": "user-cluster-01"},
                },
                {
                    "uuid": "2d46d01e-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0h",
                    "node": {"name": "user-cluster-01"},
                },
            ],
            "distribution_policy": "mac",
        },
        "enabled": True,
        "type": "lag",
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
    }
)

```
</div>
</div>

---
### Creating a LAG (ifgrp) port in a specific broadcast domain
The following output displays the record returned after the creation of a LAG port with "e0f", "e0g" and "e0h" as member ports. Also, the LAG port is added to the "Default" broadcast domain in the "Default" IPspace.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="netapp1!", verify=False):
    resource = Port()
    resource.type = "lag"
    resource.node.name = "user-cluster-01"
    resource.broadcast_domain.name = "Default"
    resource.broadcast_domain.ipspace.name = "Default"
    resource.enabled = True
    resource.lag.mode = "singlemode"
    resource.lag.distribution_policy = "mac"
    resource.lag.member_ports = [
        {"name": "e0f", "node": {"name": "user-cluster-01"}},
        {"name": "e0g", "node": {"name": "user-cluster-01"}},
        {"name": "e0h", "node": {"name": "user-cluster-01"}},
    ]
    resource.post(hydrate=True)
    print(resource)

```
<div class="try_it_out">
<input id="example8_try_it_out" type="checkbox", class="try_it_out_check">
<label for="example8_try_it_out" class="try_it_out_button">Try it out</label>
<div id="example8_result" class="try_it_out_content">
```
Port(
    {
        "broadcast_domain": {
            "ipspace": {"name": "Default"},
            "uuid": "36434bec-f70d-11e8-b145-005056bb5b8e",
            "name": "Default",
        },
        "uuid": "1807772a-fa4d-11e8-a6d7-005056bb5b8e",
        "lag": {
            "mode": "singlemode",
            "member_ports": [
                {
                    "uuid": "2d3c9adc-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0f",
                    "node": {"name": "user-cluster-01"},
                },
                {
                    "uuid": "2d40b097-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0g",
                    "node": {"name": "user-cluster-01"},
                },
                {
                    "uuid": "2d46d01e-f70d-11e8-b145-005056bb5b8e",
                    "name": "e0h",
                    "node": {"name": "user-cluster-01"},
                },
            ],
            "distribution_policy": "mac",
        },
        "enabled": True,
        "type": "lag",
        "node": {
            "name": "user-cluster-01",
            "uuid": "faa56898-f70c-11e8-b145-005056bb5b8e",
        },
    }
)

```
</div>
</div>

---
## Updating ports
You can use the network ports PATCH API to update the attributes of ports.
<br/>
---
## Examples
### Updating the broadcast domain of a port
The following PATCH request removes the port from the current broadcast domain and adds it to the specified broadcast domain.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="6867efaf-d702-11e8-994f-005056bbc994")
    resource.broadcast_domain.name = "Default"
    resource.broadcast_domain.ipspace.name = "Default"
    resource.patch()

```

---
### Updating the admin status of a port
The following PATCH request brings the specified port down.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="51d3ab39-d86d-11e8-aca6-005056bbc994")
    resource.enabled = False
    resource.patch()

```

---
### Repairing a port
The following PATCH request repairs a port. Only ports that have reachability as "repairable" can be repaired. The "reachability" parameter cannot be patched in the same request as other parameters that might affect the target port's reachability status.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="51d3ab39-d86d-11e8-aca6-005056bbc994")
    resource.reachability = "ok"
    resource.patch()

```

---
## Deleting ports
You can use the network ports DELETE API to delete VLAN and LAG ports in the cluster. Note that physical ports cannot be deleted.
Deleting a port also removes the port from the broadcast domain.
---
## Example
### Deleting a VLAN port
The network ports DELETE API is used to delete a VLAN port.
<br/>
---
```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Port

with HostConnection("<mgmt-ip>", username="admin", password="password", verify=False):
    resource = Port(uuid="6867efaf-d702-11e8-994f-005056bbc994")
    resource.delete()

```

---
"""

import asyncio
from datetime import datetime
import inspect
from typing import Callable, Iterable, List, Optional, Union

try:
    CLICHE_INSTALLED = False
    import cliche
    from cliche.arg_types.choices import Choices
    from cliche.commands import ClicheCommandError
    from netapp_ontap.resource_table import ResourceTable
    CLICHE_INSTALLED = True
except ImportError:
    pass

from marshmallow import fields, EXCLUDE  # type: ignore

import netapp_ontap
from netapp_ontap.resource import Resource, ResourceSchema, ImpreciseDateTime, Size
from netapp_ontap import NetAppResponse, HostConnection
from netapp_ontap.validations import enum_validation, len_validation, integer_validation
from netapp_ontap.error import NetAppRestError


__all__ = ["Port", "PortSchema"]
__pdoc__ = {
    "PortSchema.resource": False,
    "Port.port_show": False,
    "Port.port_create": False,
    "Port.port_modify": False,
    "Port.port_delete": False,
}


class PortSchema(ResourceSchema):
    """The fields of the Port object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", data_key="_links", unknown=EXCLUDE)
    r""" The links field of the port. """

    broadcast_domain = fields.Nested("netapp_ontap.resources.broadcast_domain.BroadcastDomainSchema", data_key="broadcast_domain", unknown=EXCLUDE)
    r""" The broadcast_domain field of the port. """

    enabled = fields.Boolean(
        data_key="enabled",
    )
    r""" The enabled field of the port. """

    lag = fields.Nested("netapp_ontap.models.port_lag.PortLagSchema", data_key="lag", unknown=EXCLUDE)
    r""" The lag field of the port. """

    mac_address = fields.Str(
        data_key="mac_address",
    )
    r""" The mac_address field of the port.

Example: 01:02:03:04:05:06 """

    metric = fields.Nested("netapp_ontap.resources.port_metrics.PortMetricsSchema", data_key="metric", unknown=EXCLUDE)
    r""" The metric field of the port. """

    mtu = Size(
        data_key="mtu",
        validate=integer_validation(minimum=68),
    )
    r""" MTU of the port in bytes. Set by broadcast domain.

Example: 1500 """

    name = fields.Str(
        data_key="name",
    )
    r""" Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)

Example: e1b """

    node = fields.Nested("netapp_ontap.resources.node.NodeSchema", data_key="node", unknown=EXCLUDE)
    r""" The node field of the port. """

    reachability = fields.Str(
        data_key="reachability",
        validate=enum_validation(['ok', 'repairable', 'not_repairable']),
    )
    r""" Reachability status of the port. Enum value "ok" is the only acceptable value for a PATCH request to repair a port.

Valid choices:

* ok
* repairable
* not_repairable """

    reachable_broadcast_domains = fields.List(fields.Nested("netapp_ontap.resources.broadcast_domain.BroadcastDomainSchema", unknown=EXCLUDE), data_key="reachable_broadcast_domains")
    r""" Reachable broadcast domains. """

    speed = Size(
        data_key="speed",
    )
    r""" Link speed in Mbps

Example: 1000 """

    state = fields.Str(
        data_key="state",
        validate=enum_validation(['up', 'down']),
    )
    r""" Operational state of the port.

Valid choices:

* up
* down """

    statistics = fields.Nested("netapp_ontap.models.port_statistics.PortStatisticsSchema", data_key="statistics", unknown=EXCLUDE)
    r""" The statistics field of the port. """

    type = fields.Str(
        data_key="type",
        validate=enum_validation(['vlan', 'physical', 'lag']),
    )
    r""" Type of physical or virtual port

Valid choices:

* vlan
* physical
* lag """

    uuid = fields.Str(
        data_key="uuid",
    )
    r""" Port UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    vlan = fields.Nested("netapp_ontap.models.port_vlan.PortVlanSchema", data_key="vlan", unknown=EXCLUDE)
    r""" The vlan field of the port. """

    @property
    def resource(self):
        return Port

    gettable_fields = [
        "links",
        "broadcast_domain.links",
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "enabled",
        "lag",
        "mac_address",
        "metric",
        "mtu",
        "name",
        "node.links",
        "node.name",
        "node.uuid",
        "reachability",
        "reachable_broadcast_domains.links",
        "reachable_broadcast_domains.ipspace",
        "reachable_broadcast_domains.name",
        "reachable_broadcast_domains.uuid",
        "speed",
        "state",
        "statistics",
        "type",
        "uuid",
        "vlan",
    ]
    """links,broadcast_domain.links,broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,enabled,lag,mac_address,metric,mtu,name,node.links,node.name,node.uuid,reachability,reachable_broadcast_domains.links,reachable_broadcast_domains.ipspace,reachable_broadcast_domains.name,reachable_broadcast_domains.uuid,speed,state,statistics,type,uuid,vlan,"""

    patchable_fields = [
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "enabled",
        "lag",
        "reachability",
    ]
    """broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,enabled,lag,reachability,"""

    postable_fields = [
        "broadcast_domain.ipspace",
        "broadcast_domain.name",
        "broadcast_domain.uuid",
        "enabled",
        "lag",
        "node.name",
        "node.uuid",
        "type",
        "vlan",
    ]
    """broadcast_domain.ipspace,broadcast_domain.name,broadcast_domain.uuid,enabled,lag,node.name,node.uuid,type,vlan,"""

def _get_field_list(field: str) -> Callable[[], List]:
    def getter():
        return [getattr(r, field) for r in Port.get_collection(fields=field)]
    return getter

async def _wait_for_job(response: NetAppResponse) -> None:
    """Examine the given response. If it is a job, asynchronously wait for it to
    complete. While polling, prints the current status message of the job.
    """

    if not response.is_job:
        return
    from netapp_ontap.resources import Job
    job = Job(**response.http_response.json()["job"])
    while True:
        job.get(fields="state,message")
        if hasattr(job, "message"):
            print("[%s]: %s" % (job.state, job.message))
        if job.state == "failure":
            raise NetAppRestError("Port modify job failed")
        if job.state == "success":
            break
        await asyncio.sleep(1)

class Port(Resource):
    """Allows interaction with Port objects on the host"""

    _schema = PortSchema
    _path = "/api/network/ethernet/ports"
    _keys = ["uuid"]

    @classmethod
    def get_collection(
        cls,
        *args,
        connection: HostConnection = None,
        max_records: int = None,
        **kwargs
    ) -> Iterable["Resource"]:
        r"""Retrieves a collection of ports (physical, VLAN and LAG) for an entire cluster.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._get_collection(*args, connection=connection, max_records=max_records, **kwargs)

    get_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get_collection.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="port show")
        def port_show(
            enabled: Choices.define(_get_field_list("enabled"), cache_choices=True, inexact=True)=None,
            mac_address: Choices.define(_get_field_list("mac_address"), cache_choices=True, inexact=True)=None,
            mtu: Choices.define(_get_field_list("mtu"), cache_choices=True, inexact=True)=None,
            name: Choices.define(_get_field_list("name"), cache_choices=True, inexact=True)=None,
            reachability: Choices.define(_get_field_list("reachability"), cache_choices=True, inexact=True)=None,
            speed: Choices.define(_get_field_list("speed"), cache_choices=True, inexact=True)=None,
            state: Choices.define(_get_field_list("state"), cache_choices=True, inexact=True)=None,
            type: Choices.define(_get_field_list("type"), cache_choices=True, inexact=True)=None,
            uuid: Choices.define(_get_field_list("uuid"), cache_choices=True, inexact=True)=None,
            fields: List[Choices.define(["enabled", "mac_address", "mtu", "name", "reachability", "speed", "state", "type", "uuid", "*"])]=None,
        ) -> ResourceTable:
            """Fetch a list of Port resources

            Args:
                enabled: 
                mac_address: 
                mtu: MTU of the port in bytes. Set by broadcast domain.
                name: Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)
                reachability: Reachability status of the port. Enum value \"ok\" is the only acceptable value for a PATCH request to repair a port.
                speed: Link speed in Mbps
                state: Operational state of the port.
                type: Type of physical or virtual port
                uuid: Port UUID
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if mac_address is not None:
                kwargs["mac_address"] = mac_address
            if mtu is not None:
                kwargs["mtu"] = mtu
            if name is not None:
                kwargs["name"] = name
            if reachability is not None:
                kwargs["reachability"] = reachability
            if speed is not None:
                kwargs["speed"] = speed
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if fields is not None:
                fields = ",".join(fields)
                kwargs["fields"] = fields

            return Port.get_collection(
                **kwargs
            )

    @classmethod
    def count_collection(
        cls,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> int:
        r"""Retrieves a collection of ports (physical, VLAN and LAG) for an entire cluster.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._count_collection(*args, connection=connection, **kwargs)

    count_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._count_collection.__doc__)

    @classmethod
    def patch_collection(
        cls,
        body: dict,
        *args,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a port.
### Related ONTAP commands
* `network port broadcast-domain add-ports`
* `network port broadcast-domain remove-ports`
* `network port ifgrp modify`
* `network port modify`
* `network port vlan modify`
* `network port reachability repair`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._patch_collection(body, *args, connection=connection, **kwargs)

    patch_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch_collection.__doc__)

    @classmethod
    def delete_collection(
        cls,
        *args,
        body: Union[Resource, dict] = None,
        connection: HostConnection = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a VLAN or LAG.
### Related ONTAP commands
* `network port ifgrp delete`
* `network port vlan delete`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._delete_collection(*args, body=body, connection=connection, **kwargs)

    delete_collection.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete_collection.__doc__)

    @classmethod
    def find(cls, *args, connection: HostConnection = None, **kwargs) -> Resource:
        r"""Retrieves a collection of ports (physical, VLAN and LAG) for an entire cluster.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._find(*args, connection=connection, **kwargs)

    find.__func__.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._find.__doc__)

    def get(self, **kwargs) -> NetAppResponse:
        r"""Retrieves the details of a physical port, VLAN, or LAG.
### Related ONTAP commands
* `network port show`
* `network port ifgrp show`
* `network port vlan show`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._get(**kwargs)

    get.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._get.__doc__)

    def post(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Creates a new VLAN (such as node1:e0a-100) or LAG (ifgrp, such as node2:a0a).
### Required properties
* `node` - Node the port will be created on.
* `type` - Defines if a VLAN or LAG will be created:
  * VLAN
    * `vlan.base_port` - Physical port or LAG the VLAN will be created on.
    * `vlan.tag` - Tag used to identify VLAN on the base port.
  * LAG
    * `lag.mode` - Policy for the LAG that will be created.
    * `lag.distribution_policy` - Indicates how the packets are distributed between ports.
    * `lag.member_ports` - Set of ports the LAG consists of.
### Optional properties
* `broadcast_domain` - The layer-2 broadcast domain the port is associated with. The port will be placed in a broadcast domain if it is not specified.  It may take several minutes for the broadcast domain to be assigned.  During that period the port cannot host interfaces.
### Related ONTAP commands
* `network port ifgrp create`
* `network port vlan create`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._post(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    post.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._post.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="port create")
        async def port_create(
            links: dict = None,
            broadcast_domain: dict = None,
            enabled: bool = None,
            lag: dict = None,
            mac_address: str = None,
            metric: dict = None,
            mtu: Size = None,
            name: str = None,
            node: dict = None,
            reachability: str = None,
            reachable_broadcast_domains: dict = None,
            speed: Size = None,
            state: str = None,
            statistics: dict = None,
            type: str = None,
            uuid: str = None,
            vlan: dict = None,
        ) -> ResourceTable:
            """Create an instance of a Port resource

            Args:
                links: 
                broadcast_domain: 
                enabled: 
                lag: 
                mac_address: 
                metric: 
                mtu: MTU of the port in bytes. Set by broadcast domain.
                name: Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)
                node: 
                reachability: Reachability status of the port. Enum value \"ok\" is the only acceptable value for a PATCH request to repair a port.
                reachable_broadcast_domains: Reachable broadcast domains.
                speed: Link speed in Mbps
                state: Operational state of the port.
                statistics: 
                type: Type of physical or virtual port
                uuid: Port UUID
                vlan: 
            """

            kwargs = {}
            if links is not None:
                kwargs["links"] = links
            if broadcast_domain is not None:
                kwargs["broadcast_domain"] = broadcast_domain
            if enabled is not None:
                kwargs["enabled"] = enabled
            if lag is not None:
                kwargs["lag"] = lag
            if mac_address is not None:
                kwargs["mac_address"] = mac_address
            if metric is not None:
                kwargs["metric"] = metric
            if mtu is not None:
                kwargs["mtu"] = mtu
            if name is not None:
                kwargs["name"] = name
            if node is not None:
                kwargs["node"] = node
            if reachability is not None:
                kwargs["reachability"] = reachability
            if reachable_broadcast_domains is not None:
                kwargs["reachable_broadcast_domains"] = reachable_broadcast_domains
            if speed is not None:
                kwargs["speed"] = speed
            if state is not None:
                kwargs["state"] = state
            if statistics is not None:
                kwargs["statistics"] = statistics
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid
            if vlan is not None:
                kwargs["vlan"] = vlan

            resource = Port(
                **kwargs
            )
            try:
                response = resource.post(hydrate=True, poll=False)
                await _wait_for_job(response)
                resource.get()
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to create Port: %s" % err)
            return [resource]

    def patch(
        self,
        hydrate: bool = False,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Updates a port.
### Related ONTAP commands
* `network port broadcast-domain add-ports`
* `network port broadcast-domain remove-ports`
* `network port ifgrp modify`
* `network port modify`
* `network port vlan modify`
* `network port reachability repair`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._patch(
            hydrate=hydrate, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    patch.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._patch.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="port modify")
        async def port_modify(
            enabled: bool = None,
            query_enabled: bool = None,
            mac_address: str = None,
            query_mac_address: str = None,
            mtu: Size = None,
            query_mtu: Size = None,
            name: str = None,
            query_name: str = None,
            reachability: str = None,
            query_reachability: str = None,
            speed: Size = None,
            query_speed: Size = None,
            state: str = None,
            query_state: str = None,
            type: str = None,
            query_type: str = None,
            uuid: str = None,
            query_uuid: str = None,
        ) -> ResourceTable:
            """Modify an instance of a Port resource

            Args:
                enabled: 
                query_enabled: 
                mac_address: 
                query_mac_address: 
                mtu: MTU of the port in bytes. Set by broadcast domain.
                query_mtu: MTU of the port in bytes. Set by broadcast domain.
                name: Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)
                query_name: Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)
                reachability: Reachability status of the port. Enum value \"ok\" is the only acceptable value for a PATCH request to repair a port.
                query_reachability: Reachability status of the port. Enum value \"ok\" is the only acceptable value for a PATCH request to repair a port.
                speed: Link speed in Mbps
                query_speed: Link speed in Mbps
                state: Operational state of the port.
                query_state: Operational state of the port.
                type: Type of physical or virtual port
                query_type: Type of physical or virtual port
                uuid: Port UUID
                query_uuid: Port UUID
            """

            kwargs = {}
            changes = {}
            if query_enabled is not None:
                kwargs["enabled"] = query_enabled
            if query_mac_address is not None:
                kwargs["mac_address"] = query_mac_address
            if query_mtu is not None:
                kwargs["mtu"] = query_mtu
            if query_name is not None:
                kwargs["name"] = query_name
            if query_reachability is not None:
                kwargs["reachability"] = query_reachability
            if query_speed is not None:
                kwargs["speed"] = query_speed
            if query_state is not None:
                kwargs["state"] = query_state
            if query_type is not None:
                kwargs["type"] = query_type
            if query_uuid is not None:
                kwargs["uuid"] = query_uuid

            if enabled is not None:
                changes["enabled"] = enabled
            if mac_address is not None:
                changes["mac_address"] = mac_address
            if mtu is not None:
                changes["mtu"] = mtu
            if name is not None:
                changes["name"] = name
            if reachability is not None:
                changes["reachability"] = reachability
            if speed is not None:
                changes["speed"] = speed
            if state is not None:
                changes["state"] = state
            if type is not None:
                changes["type"] = type
            if uuid is not None:
                changes["uuid"] = uuid

            if hasattr(Port, "find"):
                resource = Port.find(
                    **kwargs
                )
            else:
                resource = Port()
            try:
                for key, value in changes.items():
                    setattr(resource, key, value)
                response = resource.patch(poll=False)
                await _wait_for_job(response)
                resource.get(fields=",".join(changes.keys()))
                return [resource]
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to modify Port: %s" % err)

    def delete(
        self,
        body: Union[Resource, dict] = None,
        poll: bool = True,
        poll_interval: Optional[int] = None,
        poll_timeout: Optional[int] = None,
        **kwargs
    ) -> NetAppResponse:
        r"""Deletes a VLAN or LAG.
### Related ONTAP commands
* `network port ifgrp delete`
* `network port vlan delete`

### Learn more
* [`DOC /network/ethernet/ports`](#docs-networking-network_ethernet_ports)"""
        return super()._delete(
            body=body, poll=poll, poll_interval=poll_interval,
            poll_timeout=poll_timeout, **kwargs
        )

    delete.__doc__ += "\n\n---\n" + inspect.cleandoc(Resource._delete.__doc__)

    if CLICHE_INSTALLED:
        @cliche.command(name="port delete")
        async def port_delete(
            enabled: bool = None,
            mac_address: str = None,
            mtu: Size = None,
            name: str = None,
            reachability: str = None,
            speed: Size = None,
            state: str = None,
            type: str = None,
            uuid: str = None,
        ) -> None:
            """Delete an instance of a Port resource

            Args:
                enabled: 
                mac_address: 
                mtu: MTU of the port in bytes. Set by broadcast domain.
                name: Portname, such as e0a, e1b-100 (VLAN on ethernet), a0c (LAG/ifgrp), a0d-200 (vlan on LAG/ifgrp)
                reachability: Reachability status of the port. Enum value \"ok\" is the only acceptable value for a PATCH request to repair a port.
                speed: Link speed in Mbps
                state: Operational state of the port.
                type: Type of physical or virtual port
                uuid: Port UUID
            """

            kwargs = {}
            if enabled is not None:
                kwargs["enabled"] = enabled
            if mac_address is not None:
                kwargs["mac_address"] = mac_address
            if mtu is not None:
                kwargs["mtu"] = mtu
            if name is not None:
                kwargs["name"] = name
            if reachability is not None:
                kwargs["reachability"] = reachability
            if speed is not None:
                kwargs["speed"] = speed
            if state is not None:
                kwargs["state"] = state
            if type is not None:
                kwargs["type"] = type
            if uuid is not None:
                kwargs["uuid"] = uuid

            if hasattr(Port, "find"):
                resource = Port.find(
                    **kwargs
                )
            else:
                resource = Port()
            try:
                response = resource.delete(poll=False)
                await _wait_for_job(response)
            except NetAppRestError as err:
                raise ClicheCommandError("Unable to delete Port: %s" % err)


