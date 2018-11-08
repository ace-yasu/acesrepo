import hashlib
text = "grkognro32183r74g4ihhohf2f724584f4hiow"
hash = hashlib.sha256(text).hexdigest()
print hash
