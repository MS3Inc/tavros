# Also needs to be updated in galaxy.yml
VERSION = 0.1.0

clean:
	rm -f ms3_inc-troubadour-${VERSION}.tar.gz

build: clean
	ansible-galaxy collection build

install: build
	ansible-galaxy collection install --force ms3_inc-troubadour-${VERSION}.tar.gz

test:
	cd ~/.ansible/collections/ansible_collections/ms3_inc/troubadour; ansible-test integration -v --color --continue-on-error --diff --coverage
