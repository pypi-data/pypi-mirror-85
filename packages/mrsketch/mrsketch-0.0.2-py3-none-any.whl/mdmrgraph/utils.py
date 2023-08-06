

def identical(l1, l2):
	return len(l1) == len(l2) and (len(l1) == 0 or all(l1[i] == l2[i] for i in range(len(l1))))


def commonuntil(l1, l2):
	i = 0
	for i in range(len(min(l1, l2))):
		if l1[i] != l2[i]:
			break
		i += 1
	return i
