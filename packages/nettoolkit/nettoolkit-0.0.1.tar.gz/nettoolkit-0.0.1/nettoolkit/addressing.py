
# from errors import incorrectinput
incorrectinput = 'INCORRECT SUBNET OR SUBNET MASK DETECTED NULL RETURNED'

# ----------------------------------------------------------------------------
# Module Functions
# ----------------------------------------------------------------------------


def addressing(subnet):
	'''main function proiving ip-subnet object for various functions on it
	--> ipsubnet object

	:param: subnet: either ipv4 or ipv6 subnet with /mask
	:param type: str

	:param decmask: decimal mask notation only in case of IPv4 (optional)
	:param type: str
	'''
	v_obj = Validation(subnet)
	if v_obj.validated:
		version = v_obj.version
		if version == 4:
			return IPv4(v_obj.subnet)
		elif version == 6:
			return IPv6(v_obj.subnet)

# private
# Concatenate strings s and pfx with conjuction
def _strconcate(s, pfx, conj=''):
	if s == '':	
		s = s + pfx
	else:
		s = s + conj + pfx
	return s

def found(s, sub, pos=0):
	'''Search for substring in string and return Boolean result
	--> bool

	:param: s: main string to be search within
	:param type: str

	:param: sub: substring which is to be search in to main string
	:param type: str

	:param: pos: position index, search to be start from
	:param type: int
	'''
	try:
		return True if s.find(sub, pos) > -1 else False
	except:
		return False


# ----------------------------------------------------------------------------
# Validation Class - doing subnet validation and version detection
# ----------------------------------------------------------------------------
class Validation():
	'''ip-subnet validation class
	:param subnet: ipv4 or ipv6 subnet with "/" mask
	:param type: str

	'''

	def __init__(self, subnet):
		'''ip-subnet validation class
		:param subnet: ipv4 or ipv6 subnet with "/" mask
		:param type: str

		'''
		self.mask = None
		self.subnet = subnet
		self.version = self.__function
		self.validated = False
		if self.version == 4:
			self.validated = self.check_v4_input
		elif self.version == 6:
			self.validated = self.check_v6_input
		else:
			raise Exception(f"Not a VALID Subnet {subnet}")

	@property
	def __function(self):
		if found(self.subnet, ":"):
			return 6
		elif found(self.subnet, "."):
			return 4
		else:
			return 0

	@property
	def check_v4_input(self):
		'''Property to validate provided v4 subnet
		'''
		# ~~~~~~~~~ Mask Check ~~~~~~~~~
		try:
			self.mask = self.subnet.split("/")[1]
		except:
			self.mask = 32
			self.subnet = self.subnet + "/32"
		try:			
			self.mask = int(self.mask)
			if not all([self.mask>=0, self.mask<=32]):
				raise Exception(f"Invalid mask length {self.mask}")
		except:
			raise Exception(f"Incorrect Mask {self.mask}")

		# ~~~~~~~~~ Subnet Check ~~~~~~~~~
		try:
			octs = self.subnet.split("/")[0].split(".")
			if len(octs) != 4:
				raise Exception(f"Invalid Subnet Length {len(octs)}")
			for i in range(4):
				if not all([int(octs[i])>=0, int(octs[i])<=255 ]):
					raise Exception("Invalid Subnet Octet {i}")
			return True
		except:
			raise Exception("Unidentified Subnet")

	@property
	def check_v6_input(self):
		'''Property to validate provided v6 subnet
		'''
		try:
			# ~~~~~~~~~ Mask Check ~~~~~~~~~
			self.mask = self.subnet.split("/")[1]
		except:
			self.mask = 128
			self.subnet = self.subnet + "/128"
		try:
			self.mask = int(self.mask)
			if not all([self.mask>=0, self.mask<=128]):
				raise Exception(f"Invalid mask length {self.mask}")
			
			# ~~~~~~~~~ Subnet ~~~~~~~~~
			sip = self.subnet.split("/")[0].split("::")
			
			# ~~~~~~~~~ Check Subnet squeezers ~~~~~~~~~
			if len(sip) > 2:
				raise Exception("Invalid Subnet, Squeezers detected > 1")
			
			# ~~~~~~~~~ Subnet Length ~~~~~~~~~
			lsip = sip[0].split(":")
			try:
				rsip = sip[1].split(":")
			except:
				rsip = []
			if len(lsip)+len(rsip) > 8:
				raise Exception(f"Invalid Subnet Length {len(lsip)+len(rsip)}")
			
			# ~~~~~~~~~ Validate Hextates ~~~~~~~~~
			for hxt in lsip+rsip:
				try:
					if hxt != '' :
						hex(int(hxt, 16))
				except:
					raise Exception(f"Invalid Hextate {hxt}")
			
			# ~~~~~~~~~ All Good ~~~~~~~~~
			return True

		except:
			raise Exception("Unidentified Subnet")


# ----------------------------------------------------------------------------
# IPv4 Subnet (IPv4) class 
# ----------------------------------------------------------------------------
class IPv4:
	'''Defines IPv4 object and its various operations'''

	# Initializer
	def __init__(self, subnet):
		self.subnet = subnet
		self.mask = int(self.subnet.split("/")[1])
		self.net = self.subnet.split("/")[0]		

	def __str__(self): return self.subnet
	def __repr__(self): return self.subnet

	def __getitem__(self, n):
		'''get a specific ip, Range of IP(s) from Subnet'''
		try:
			return self.n_thIP(n, False)
		except:
			l = []
			for x in self.__subnetips(n.start, n.stop):
				l.append(x)
			return tuple(l)

	def __add__(self, n):
		'''add n-ip's to given subnet and return udpated subnet'''
		return self.n_thIP(n, False, "_")

	def __sub__(self, n):
		'''Deduct n-ip's from given subnet and return udpated subnet'''
		return self.n_thIP(-1*n, False, "_")

	def __truediv__(self, n):
		'''Devide provided subnet/super-net to n-number of smaller subnets'''
		return self.__sub_subnets(n)

	def __iter__(self):
		'''iterate over full subnet'''
		return self.__subnetips()

	# ------------------------------------------------------------------------
	# Private Properties
	# ------------------------------------------------------------------------

	# binary to decimal mask convert
	def __bin2decmask(self, binmask):
		return binmask.count('1')

	# binary mask return property
	@property
	def __binmask(self):
		try:
			pone ='1'*self.mask
			pzero = '0'*(32-self.mask)
			return pone+pzero
		except:
			pass

	# Inverse mask return property
	@property
	def __invmask(self):
		try:
			pone ='0'*self.mask
			pzero = '1'*(32-self.mask)
			return pone+pzero
		except:
			pass


	# ------------------------------------------------------------------------
	# Private Methods
	# ------------------------------------------------------------------------

	# binary to Decimal convert subnet method
	@staticmethod
	def __bin2dec(binnet):
		o = []
		for x in range(0, 32, 8):
			o.append(int(binnet[x:x+8], 2))
		return o

	# binary subnet return method
	@staticmethod
	def __binsubnet(subnet):
		try:
			s = ''
			octs = subnet.split("/")[0].split(".")
			for o in octs:
				bo = str(bin(int(o)))[2:]
				lbo = len(bo)
				pzero = '0'*(8 - lbo)
				s = s + pzero + bo
			return s
		except:
			pass

	# adjust length of 4 octets
	@staticmethod
	def __set32bits(bins):
		lbo = len(str(bins))
		pzero = '0'*(34 - lbo)
		return pzero+bins[2:]

	# list to octet conversion
	@staticmethod
	def __lst2oct(lst):
		l = ''
		for x in lst:
			l = str(x) if l == '' else l +'.'+ str(x)
		return l

	# compare two binary for and operation
	def __both(self, binone, bintwo):
		b1 = int(binone.encode('ascii'), 2)
		b2 = int(bintwo.encode('ascii'), 2) 
		b1b2 = bin(b1 & b2)
		return self.__set32bits(b1b2)

	# compare two binary for or operation
	def __either(self, binone, bintwo):
		b1 = int(binone.encode('ascii'), 2)
		b2 = int(bintwo.encode('ascii'), 2) 
		b1b2 = bin(b1 | b2)
		return self.__set32bits(b1b2)

	# get n-number of subnets of given super-net
	def __sub_subnets(self, n):
		_iplst = []
		for i1, x1 in enumerate(range(32)):
			p = 2**x1
			if p >= n: break
		_nsm = self.mask + i1
		_nip = int(self.__binsubnet(self.NetworkIP()), 2)
		_bcip = int(self.__binsubnet(self.BroadcastIP()), 2)
		_iis = (_bcip - _nip + 1) // p
		for i2, x2 in enumerate(range(_nip, _bcip, _iis)):
			_iplst.append(self.n_thIP(i2*_iis)+ "/" + str(_nsm))
		return tuple(_iplst)

	# yields IP Address(es) of the provided subnet
	def __subnetips(self, begin=0, end=0):
		_nip = int(self.__binsubnet(self.NetworkIP()), 2)
		if end == 0:
			_bcip = int(self.__binsubnet(self.BroadcastIP()), 2)
		else:
			_bcip = _nip + (end-begin)
		for i2, x2 in enumerate(range(_nip, _bcip)):
			if begin>0:  i2 = i2+begin
			yield self.n_thIP(i2)

	# ------------------------------------------------------------------------
	# Available Methods & Public properties of class
	# ------------------------------------------------------------------------

	def NetworkIP(self, withMask=True):
		'''Network IP Address of subnet from provided IP/Subnet'''
		try:
			s = self.__binsubnet(self.subnet)
			bm = self.__binmask
			net = self.__lst2oct(self.__bin2dec(self.__both(s, bm )))
			if withMask :
				return net + "/" + str(self.mask)
			else:
				return net
		except:
			pass
	subnetZero = NetworkIP

	def BroadcastIP(self, withMask=False):
		'''Broadcast IP Address of subnet from provided IP/Subnet'''
		try:
			s = self.__binsubnet(self.subnet)
			im = self.__invmask
			bc = self.__lst2oct(self.__bin2dec(self.__either(s, im )))
			if withMask :
				return bc + "/" + str(self.mask)
			else:
				return bc
		except:
			pass

	def n_thIP(self, n=0, withMask=False, _=''):
		'''n-th IP Address of subnet from provided IP/Subnet'''
		s = self.__binsubnet(self.subnet)
		if _ == '':
			bm = self.__binmask
			addedbin = self.__set32bits(bin(int(self.__both(s, bm), 2)+n))
		else:
			addedbin = self.__set32bits(bin(int(s.encode('ascii'), 2 )+n))

		if any([addedbin > self.__binsubnet(self.BroadcastIP()), 
				addedbin < self.__binsubnet(self.NetworkIP())]) :
			raise Exception("Address Out of Range")
		else:
			ip = self.__lst2oct(self.__bin2dec(addedbin))
			if withMask :
				return ip + "/" + str(self.mask)
			else:
				return ip

	@property
	def decmask(self):
		'''Decimal Mask from provided IP/Subnet - Numeric/Integer'''
		return self.mask
	decimalMask = decmask

	@property
	def binmask(self):
		'''Binary Mask from provided IP/Subnet'''
		return self.__lst2oct(self.__bin2dec(self.__binmask))

	@property
	def invmask(self):
		'''Inverse Mask from provided IP/Subnet'''
		return self.__lst2oct(self.__bin2dec(self.__invmask))

	def ipdecmask(self, n=0):
		'''IP with Decimal Mask for provided IP/Subnet,
		n ==>
		n-th ip of subnet will appear in output if provided,
		subnet0 ip will appear in output if not provided
		default: n = 0, for Network IP
		'''
		try:
			return self[n] + "/" + str(self.mask)
		except:
			raise Exception(f'Invalid Input : detected')

	def ipbinmask(self, n=0):
		'''IP with Binary Mask for provided IP/Subnet,
		n ==>
		n-th ip of subnet will appear in output if provided,
		same input subnet/ip will appear in output if not provided
		set - n = 0, for Network IP
		'''
		try:
			return self[n] + " " + self.binmask
		except:
			raise Exception(f'Invalid Input : detected')

	def ipinvmask(self, n=0):
		'''IP with Inverse Mask for provided IP/Subnet,
		n ==>
		n-th ip of subnet will appear in output if provided,
		same input subnet/ip will appear in output if not provided
		set - n = 0, for Network IP
		'''
		try:
			return self[n] + " " + self.invmask
		except:
			raise Exception(f'Invalid Input : detected')

	@property
	def version(self):
		'''get version of IP Subnet'''
		return 4

# ----------------------------------------------------------------------------
# IP Subnet (IPv6) class 
# ----------------------------------------------------------------------------

class IPv6:
	'''Defines IPv6 object and its various operations'''

	# Object Initializer
	def __init__(self, subnet=''):
		self.subnet = subnet
		self.__networkIP
		self.__actualv6subnet = False				# breaked subnet expanded
		self.__NetworkAddressbool = False			# Subnet zero available/not
		self.mask = int(self.subnet.split("/")[1])
		self.net = self.subnet.split("/")[0]

	def __str__(self): return self.subnet
	def __repr__(self): return self.subnet

	def __getitem__(self, n):
		'''get a specific ip, Range of IP(s) from Subnet'''
		try:
			return self.n_thIP(n, False)
		except:
			l = []
			for x in self.__subnetips(n.start, n.stop):
				l.append(x)
			return tuple(l)

	def __add__(self, n):
		'''add n-ip's to given subnet and return udpated subnet'''
		return self.n_thIP(n, False, "_")

	def __sub__(self, n):
		'''Deduct n-ip's from given subnet and return udpated subnet'''
		return self.n_thIP(-1*n, False, "_")

	def __truediv__(self, n):
		'''Devide provided subnet/super-net to n-number of smaller subnets'''
		return self.__sub_subnets(n)

	def __iter__(self):
		'''iterate over full subnet'''
		return self.__subnetips()


	# ------------------------------------------------------------------------
	# Private Methods
	# ------------------------------------------------------------------------

	# get n-number of subnets of given super-net
	def __sub_subnets(self, n):
		_iplst = []
		for i1, x1 in enumerate(range(128)):
			p = 2**x1
			if p >= n: break
		_nsm = self.mask + i1
		_nip = int(self.__binsubnet(self.subnetZero()), 2)
		_bcip = int(self.__binsubnet(self.BroadcastIP()), 2)
		_iis = (_bcip - _nip + 1) // p
		for i2, x2 in enumerate(range(_nip, _bcip, _iis)):
			_iplst.append(self.n_thIP(i2*_iis)+ "/" + str(_nsm))
		return tuple(_iplst)

	# binary subnet return method
	@staticmethod
	def __binsubnet(subnet):
		try:
			s = ''
			octs = subnet.split("/")[0].split(":")
			for o in octs:
				bo = str(bin(int(o, 16)))[2:]
				lbo = len(bo)
				pzero = '0'*(16 - lbo)
				s = s + pzero + bo
			return s
		except:
			pass

	# yields IP Address(es) of the provided subnet
	def __subnetips(self, begin=0, end=0):
		_nip = int(self.__binsubnet(self.subnetZero()), 2)
		if end == 0:
			_bcip = int(self.__binsubnet(self.BroadcastIP()), 2)
		else:
			_bcip = _nip + (end-begin)
		for i2, x2 in enumerate(range(_nip, _bcip)):
			if begin>0:  i2 = i2+begin
			yield self.n_thIP(i2)

	# update Subnet to actual length
	@property
	def __actualsize(self):
		try:
			if not self.__actualv6subnet:
				p = ''
				sip = self.subnet.split("/")[0].split("::")
				if len(sip) == 2:
					# ~~~~~~ No padding, inserting zeros in middle ~~~~~~~
					for x in range(1, 9):
						p = _strconcate(p, self.__getHext(hexTnum=x), conj=':')
					self.subnet = p
				else :
					# ~~~~~~~ pad leading zeros ~~~~~~~
					lsip = sip[0].split(":")
					for x in range(8-len(lsip), 0, -1):
						p = _strconcate(p, '0', conj=":")
					if p != '':
						self.subnet = p + ':' + self.subnet
				self.__actualv6subnet = True
		except:
			return False


	# IP Portion of Input
	@property
	def __networkIP(self):
		try:
			self.network = self.subnet.split("/")[0]
			return self.network
		except:
			raise Exception("WARNING!!!   NO SUBNET DETECTED, NULL RETURNED")
			return None


	# Padding subnet with ":0" or ":ffff"
	@staticmethod
	def __pad(padwhat='0', counts=0):
		s = ''
		for x in range(counts):
			s = s + ":" + padwhat
		return s


	# Return a specific Hextate (hexTnum) from IPV6 address
	def __getHext(self, hexTnum, s=''):	
		if s == '':
			s = self.subnet.split("/")[0]
		try:
			if s != '' and all([hexTnum>0, hexTnum<=8]):
				sip = s.split("/")[0].split("::")
				lsip = sip[0].split(":")
				if hexTnum <= len(lsip):
					return lsip[hexTnum-1]
				else:
					rsip = sip[1].split(":")
					if rsip[0] == '': rsip = []
					if 8-hexTnum < len(rsip):
						return rsip[(9-hexTnum)*-1]
					else:
						return '0'
			else:
				raise Exception(incorrectinput)
				return None
		except:
			raise Exception(incorrectinput)
			return None


	# Return Number of Network Hextates (hxts) from IPV6 address
	def __getHextates(self, hxts=1, s=''):
		ox = ''
		for o in range(1, hxts+1):
			ox = _strconcate(ox, self.__getHext(o, s=s), conj=':')
		return ox+":"


	# NETWORK / BC Address Calculation : addtype = 'NET' , 'BC'
	def __NetORBcaddress(self, addtype='NET'):
		self.__actualsize
		if self.mask != '' and self.mask<128:	 # Non host-only subnets
			x = 0 if addtype == 'NET' else -1
			padIP = '0' if addtype == 'NET' else 'ffff'
			(asilast, avs) = ([], [])
			fixedOctets = self.mask//16

			## get full list of available subnets in selected Hexate.
			while x < 65536:	
				asilast.append(x)
				x = x + (2**(16-(self.mask-((fixedOctets)*16))))

			## check avlbl subnet and choose less then given one.			
			for netx in asilast:		
				avs.append(self.__getHextates(fixedOctets)  
										+ str(hex(netx))[2:])
				if addtype =='BC':
					last_subnet = avs[-1]
				if int(self.__getHext(fixedOctets+1), 16) < netx:
					break
				if addtype =='NET':
					last_subnet = avs[-1]

			## Return subnet by padding zeros.
			self.fixedOctets = fixedOctets
			return last_subnet+self.__pad(padIP, 7-fixedOctets)	

		else:									# host-only subnet
			return self.network

	# ------------------------------------------------------------------------
	# Available Methods & Public properties of class
	# ------------------------------------------------------------------------

	# Return a specific Hextate (hexTnum) from IPV6 address
	def getHext(self, hexTnum):
		return self.__getHext(hexTnum)

	@property
	def NetworkAddress(self):
		'''-->Returns only NETWORK ADDRESS for given subnet'''
		if not self.__NetworkAddressbool:
			self._subneTzero = self.__NetORBcaddress(addtype='NET')
			self.__NetworkAddressbool = True
		return self._subneTzero

	def subnetZero(self, withMask=True):
		'''--> Network Address with/without mask for given subnet
		'''
		if withMask :
			return self.NetworkAddress + "/" + str(self.mask)
		else:
			return self.NetworkAddress


	def BroadcastIP(self, withMask=True):
		'''--> Broadcast Address with/without mask for given subnet
		'''
		if withMask :
			return self.BroadcastAddress + "/" + str(self.mask)
		else:
			return self.BroadcastAddress

	def n_thIP(self, n=0, withMask=False, _=''):
		'''--> n-th IP with/without mask from given subnet
		'''
		ip = self.addIPtoNetwork(n, _)
		mask = self.decimalMask
		return ip+"/"+mask if withMask else ip

	@property
	def decimalMask(self):
		'''--> decimal mask of given subnet'''
		return str(self.mask)

	@property
	def binmask(self):
		'''--> None for IPV6 '''
		return None
	@property
	def invmask(self):
		'''--> None for IPV6 '''
		return None
	def ipdecmask(self, n=0):
		'''--> None for IPV6 '''
		return self.n_thIP(n, True)
	def ipbinmask(self, n=0):
		'''--> None for IPV6 '''
		return None
	def ipinvmask(self, n=0):
		'''--> None for IPV6 '''
		return None

	@property
	def BroadcastAddress(self):
		'''-->Returns BROADCAST ADDRESS for given subnet'''
		return self.__NetORBcaddress(addtype='BC')


	def addIPtoNetwork(self, num=0, _=''):
		'''-->Adds num of IP to Network IP and return address'''
		self.NetworkAddress
		s = self._subneTzero
		if _ != '':
			s = self.subnet
		_7o = self.__getHextates(7, s)
		_8o = int(self.__getHext(8, s)) + num
		return _7o + str(hex(_8o)[2:])

	@property
	def version(self):
		'''get version of IP Subnet'''
		return 6

# ----------------------------------------------------------------------------
# Main Function
# ----------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# END
# ----------------------------------------------------------------------------
