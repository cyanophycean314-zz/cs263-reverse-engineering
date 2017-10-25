# You may change anything in this file except the test-related rules.


CFLAGS=-std=c11 -O2 -Wall -Werror

NOSEFLAGS=-v -s

.PHONY: all
all: hasher cracker

.PHONY: clean
clean:
	rm -f \
		hashpw.o \
		hasher \
		crackpw.o \
		cracker \
	;

hashpw.o: hashpw.c
	gcc $(CFLAGS) -c -o hashpw.o hashpw.c

hasher: hashpw.o hasher.c
	gcc $(CFLAGS) -o hasher hashpw.o hasher.c

crackpw.o: crackpw.c
	gcc $(CFLAGS) -c -o crackpw.o crackpw.c

cracker: hashpw.o crackpw.o cracker.c
	gcc $(CFLAGS) -o cracker hashpw.o crackpw.o cracker.c

.PHONY: test
test: assert_pyvers assert_nose assert_data_size hasher cracker
	python3 -m nose $(NOSEFLAGS) tests/tests.py

.PHONY: test_keys
test_keys: assert_pyvers assert_nose
	python3 -m nose $(NOSEFLAGS) tests/tests.py:test_keys

.PHONY: test_hasher
test_hasher: assert_pyvers assert_nose hasher
	python3 -m nose $(NOSEFLAGS) tests/tests.py:test_hasher

.PHONY: test_cracker
test_cracker: assert_pyvers assert_nose assert_data_size cracker
	python3 -m nose $(NOSEFLAGS) tests/tests.py:test_cracker

.PHONY: test_network_cracker
test_network_cracker: assert_pyvers assert_nose assert_data_size
	python3 -m nose $(NOSEFLAGS) tests/tests.py:test_network_cracker

.PHONY: assert_pyvers
assert_pyvers:
	python3 -c 'import sys; assert sys.version_info[1] >= 4'

.PHONY: assert_nose
assert_nose:
	python3 -c 'import nose'

.PHONY: assert_data_size
assert_data_size:
	data/.check_data_size.sh
