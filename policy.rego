package opa.examples

import data.networks
import data.ports
import data.servers

public_servers contains server if {
	some k, 
	server := servers[_]
	server.ports[_] == ports[k].id
	ports[k].networks[_] == networks[m].id
	networks[m].public == true
}