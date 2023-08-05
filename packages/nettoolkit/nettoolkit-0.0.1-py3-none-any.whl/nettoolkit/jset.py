# -----------------------------------------------------------------------------
# IMPORTS
# -----------------------------------------------------------------------------

from .gpl import Default, STR, Container

# ---------------------------------------------------------------------------- #
# J-Set
# ---------------------------------------------------------------------------- #

class JSet(Default, STR, Container):
	"""Juniper Standard to set converter"""

	def __init__(self, input_file=None, input_list=None):
		self.output = []
		self.err = False
		if input_file or input_list: self.set_input(input_file, input_list)

	@property
	def objVar(self): return self.output

	def set_input(self, input_file=None, input_list=None):
		"""set input list from either provided input.
		--> None

		:param input_file: input text file i/o
		:type input_file: i/o

		:param input_list: input in format of list or tuple
		:type input_list: list, tuple
		"""
		if not input_file and not input_list:
			pass
		elif input_file:
			self.read_input_file(input_file)
		elif input_list:
			self.read_input_list(input_list)

	@property
	def to_set(self):
		"""reads juniper standard config and convert it to set, store it to output
		--> None
		"""
		varL, varS, varR, c = "", "set ", [], 0
		try :
			for line in self.lst:
				c += 1
				l = line.strip()
				# operate
				l = self.delete_trailing_remarks(l) 					# Remove Trailing remarks
				llen = len(l)
				if l[:1] == "#" or self.right(l, 1) == "/" : continue 	# Remark lines - bypass
				elif len(l) == 0 : continue								# Empty lines - bypass
				elif self.right(l, 1) == "{" :							# Hierarchical config follows
					varR.append(varL)
					varL = varL.strip() + " " + l[:llen - 1]
				elif self.right(l, 1) == "}" :							# Hierarchical config ends
					varL = varR[len(varR)-1]
					varR.pop()
				# elif self.right(l, 12) == " SECRET-DATA" :				# Remove encrypted password remark
				# 	self.output.append(varS + varL.strip() + " " + l[:llen - 17])
				elif self.right(l, 1) == ";" :							# Terminal lines
					# Lines consisting Multi section parameters [ ]
					if self.right(l[:llen-1].strip(), 1) == "]" :
						bbs = l.find("[") + 1
						bbe = l.find("]") + 1
						text_string = self.mid(l, bbs + 2, bbe - bbs - 3)
						wrdArray = text_string.split(" ")
						varEX = l[:bbs - 1]
						# Count of parameters inside  []
						for eachitem in wrdArray:
							tmp_l = varS+varL.strip()+" "+varEX+" "+eachitem
							self.output.append(tmp_l)
					# Normal lines
					else :
						self.output.append(varS+varL.strip()+" "+l[:llen - 1])
				else :													# Uncategorized Lines 
					self.err = True
					raise Exception(f"UndefinedTypeLine-{c}:{line}")
		except :
			self.err = True
			raise Exception(f"ErrorParsingLine-{c}:{line}")

	def read_input_list(self, input_list):
		"""Reads input list as input list
		--> None

		:param input_list: input in format of list or tuple
		:type input_list: list, tuple
		"""
		if isinstance(input_list, (list, tuple)):
			self.lst = input_list
		else:
			raise Exception(f"InputListReadError")

	def read_input_file(self, input_file):
		"""Reads input file and set input list
		--> None

		:param input_file: input text file i/o
		:type input_file: i/o
		"""
		try:
			with open(input_file, "r") as f:
				self.lst = f.readlines()
		except:
			raise Exception(f"InputFileReadError-{input_file}")
# ---------------------------------------------------------------------------- #

