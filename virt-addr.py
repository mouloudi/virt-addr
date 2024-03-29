#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import subprocess
import sys
import xml.etree.cElementTree as etree

import libvirt


logging.basicConfig(format='%(levelname)s:%(funcName)s:%(message)s',
                    level=logging.INFO)

parser = etree.XMLParser()

conn = libvirt.openReadOnly(None)
if conn is None:
    logging.error('Failed to open connection to the hypervisor')
    sys.exit(1)

domain = conn.lookupByName(sys.argv[1])
desc = etree.fromstring(domain.XMLDesc(0))
macAddr = desc.find(
    "devices/interface[@type='network']/mac").attrib["address"].lower().strip()
logging.debug("XMLDesc = %s", macAddr)

output = subprocess.Popen(["arp", "-n"],
                          stdout=subprocess.PIPE).communicate()[0]
lines = [line.split() for line in output.split("\n")[1:]]
logging.debug(lines)

IPaddr = [line[0] for line in lines if (line and (line[2] == macAddr))]
if IPaddr:
    print(IPaddr[0])
