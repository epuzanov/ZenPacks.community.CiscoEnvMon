################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoExpansionCardMap

CiscoExpansionCardMap maps the cardTable table to cards objects

$Id: CiscoExpansionCardMap.py,v 1.0 2010/12/08 21:51:11 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import SnmpPlugin, GetTableMap
from Products.DataCollector.plugins.DataMaps import MultiArgs

class CiscoExpansionCardMap(SnmpPlugin):
    """Map Cisco Chassis Card table to model."""

    maptype = "CiscoExpansionCardMap"
    modname = "ZenPacks.community.CiscoEnvMon.CiscoExpansionCard"
    relname = "cards"
    compname = "hw"

    snmpGetTableMaps = (
        GetTableMap('cardTable',
                    '.1.3.6.1.4.1.9.3.6.11.1',
                    {
                        '.3': 'setProductKey',
                        '.4': 'serialNumber',
                        '.5': 'HWVer',
                        '.6': 'FWRev',
                        '.7': 'slot',
                        '.8': '_cbi',
                        '.9': 'state',
                    }
        ),
    )

    states  =  {1:'unknown',
                2:'up',
                3:'down',
                4:'standby',
                }

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
        rm = self.relMap()
        for oid, card in tabledata.get("cardTable",{}).iteritems():
            try:
                om = self.objectMap(card)
                om.snmpindex = oid.strip('.')
                if int(getattr(om, '_cbi', 0)) != 0:
                    try:
                        pslot = tabledata["cardTable"][str(om._cbi)]["slot"]
                        om.slot = "%02d.%s"%(pslot, om.slot)
                    except: continue
                else:
                    om.slot = "%02d"%om.slot
                om.id = self.prepId(om.slot)
                om.setProductKey = MultiArgs(om.setProductKey, 'Cisco')
                om.state = self.states.get(int(om.state), 'unknown')
            except AttributeError:
                continue
            rm.append(om)
        return rm
