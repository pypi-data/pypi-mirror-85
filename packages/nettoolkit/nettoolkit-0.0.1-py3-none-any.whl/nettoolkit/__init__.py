__doc__ = '''Tool Set for Networking Geeks
-------------------------------------------------------------------
JSet, IPv4, IPv6, addressing, Validation,
Default, Container, Numeric, STR, IO, LST, DIC, LOG, DB, IP
-------------------------------------------------------------------
 JSet         convert juniper standard config to set config
 IPv4         IPV4 Object, and its operations
 IPv6         IPV4 Object, and its operations
 addressing   dynamic allocation of IPv4/IPv6 Objects
 Validation   Validate subnet
 Default      default implementations of docstring
 Container    default identical dunder methods implementations
 Numeric      To be implemented later
 STR          String Operations static methods 
 IO           Input/Output of text files Operations static methods 
 LST          List Operations static methods 
 DIC          Dictionary Operations static methods 
 LOG          Logging Operations static methods 
 DB           Database Operations static methods 
 IP           IP Addressing Operations static methods 
-------------------------------------------------------------------
'''

__all__ = ['JSet', 
	'IPv4', 'IPv6', 'addressing', 'Validation',
	'Default', 'Container', 'Numeric', 'STR', 'IO', 'LST', 'DIC', 'LOG', 'DB', 'IP']

__version__ = "0.0.1"

from .jset import JSet
from .addressing import IPv4, IPv6, addressing, Validation
from .gpl import Default, Container, Numeric, STR, IO, LST, DIC, LOG, DB, IP





