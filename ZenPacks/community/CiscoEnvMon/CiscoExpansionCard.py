################################################################################
#
# This program is part of the CiscoEnvMon Zenpack for Zenoss.
# Copyright (C) 2010 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""CiscoExpansionCard

CiscoExpansionCard is an abstraction of a PCI card.

$Id: CiscoExpansionCard.py,v 1.0 2010/12/13 18:19:38 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from Products.ZenModel.ExpansionCard import ExpansionCard
from Products.ZenModel.ZenossSecurity import *

class CiscoExpansionCard(ExpansionCard):
    """Cisco ExpansionCard object"""

    portal_type = meta_type = 'CiscoExpansionCard'

    state = "unknown"
    HWVer = "unknown"
    FWRev = "unknown"
    monitor = True

    _properties = ExpansionCard._properties + (
        {'id':'state', 'type':'string', 'mode':'w'},
        {'id':'HWver', 'type':'string', 'mode':'w'},
        {'id':'FWRev', 'type':'string', 'mode':'w'},
    )

    factory_type_information = (
        {
            'id'             : 'CiscoExpansionCard',
            'meta_type'      : 'CiscoExpansionCard',
            'description'    : """Arbitrary device grouping class""",
            'icon'           : 'ExpansionCard_icon.gif',
            'product'        : 'CiscoMon',
            'factory'        : 'manage_addCiscoExpansionCard',
            'immediate_view' : 'viewCiscoExpansionCard',
            'actions'        :
            ( 
                { 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewCiscoExpansionCard'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'perfConf'
                , 'name'          : 'Template'
                , 'action'        : 'objTemplates'
                , 'permissions'   : (ZEN_CHANGE_DEVICE, )
                },
                { 'id'            : 'viewHistory'
                , 'name'          : 'Modifications'
                , 'action'        : 'viewHistory'
                , 'permissions'   : (ZEN_VIEW_MODIFICATIONS,)
                },
            )
          },
        )

    def statusDot(self, status=None):
        """
        Return the Dot Color based on maximal severity
        """
        colors = {0:'green',1:'purple',2:'blue',3:'yellow',4:'orange',5:'red'}
        if not self.monitor: return 'grey'
        severity = self.ZenEventManager.getMaxSeverity(self)
        return colors.get(severity, 'grey')

    def statusString(self, status=None):
        """
        Return the status string
        """
        return self.state or 'Unknown'

InitializeClass(CiscoExpansionCard)
