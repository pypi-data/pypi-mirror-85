cdef extern from "<math.h>":
	cdef double log2(double)
	cdef double log10(double)

cdef extern from "<stdlib.h>":
	cdef void memset(void*, int, size_t)

cdef extern from "<stdio.h>":
	cdef void printf(const char *, ...)

cdef struct ent_t:
	size_t ccount[256]
	size_t totalc

cdef ent_init(ent_t* ent):
	memset(ent, 0, sizeof(ent_t))

cdef ent_update(ent_t *ent, unsigned char *data, size_t length):
	cdef size_t i = 0
	for i in range(length):
		ent.ccount[data[i]] += 1
	ent.totalc += length

cdef double ent_final(ent_t *ent):
	cdef size_t i = 0
	cdef double prob[256]
	cdef double entropy = 0

	memset(prob, 0, sizeof(prob))

	for i in range(256):
		prob[i] = ent.ccount[i] / ent.totalc
		if prob[i]:
			entropy += prob[i] * log2(1.0 / prob[i])

	return entropy

def ent(data):
	cdef ent_t ent
	ent_init(&ent)

	if isinstance(data, (bytes, bytearray)):
		ent_update(&ent, data, len(data))
		return ent_final(&ent)

	elif hasattr(data, 'read'):
		while True:
			buff = data.read(4096)
			if not buff:
				break
			ent_update(&ent, buff, len(buff))
		return ent_final(&ent)
