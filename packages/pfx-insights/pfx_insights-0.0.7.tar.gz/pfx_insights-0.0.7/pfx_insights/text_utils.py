import string
import unicodedata

class TextUtils:
	def encode_text(self, text_to_encode):
		if text_to_encode == None:
			return ''

		return " ".join(str(unicodedata.normalize('NFKD', text_to_encode).encode('ascii', 'replace').decode('utf8')).strip().lower().split())