# Copyright (c) 2020 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.

SVC=justice-augment-python-sdk
BUILDER=$(SVC)-builder
VERSION=$(shell node -p "require('./version.json').version")

RUN=docker run --rm \
	-v $(CURDIR):/workspace/$(SVC) \
	-w /workspace/$(SVC)

.PHONY: init test

build:
	docker build -t $(BUILDER) .
	$(RUN) $(BUILDER) cp tox.ini tox.orig.ini
	@$(RUN) $(BUILDER) sed -i 's/<ADMIN_USERNAME>/${ADMIN_USERNAME}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<ADMIN_PASSWORD>/${ADMIN_PASSWORD}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<IAM_CLIENT_ID>/${IAM_CLIENT_ID}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<IAM_CLIENT_SECRET>/${IAM_CLIENT_SECRET}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<BUILTIN_DB_USER_NAME>/${BUILTIN_DB_USER_NAME}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<BUILTIN_DB_USER_PASSWORD>/${BUILTIN_DB_USER_PASSWORD}/g' tox.ini
	@$(RUN) $(BUILDER) sed -i 's/<BUILTIN_DB_NAME>/${BUILTIN_DB_NAME}/g' tox.ini

clean:
	$(RUN) $(BUILDER) cp -f tox.orig.ini tox.ini
	$(RUN) $(BUILDER) rm tox.orig.ini

COMPOSE_TEST=docker-compose -f docker-compose-test.yaml
test:
	$(COMPOSE_TEST) up -d -V
	sleep 30
	-$(COMPOSE_TEST) run test tox
	$(COMPOSE_TEST) down --remove-orphans

# Publish to PyPI
publish:
	pip install twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf build dist .egg requests.egg-info

# Create git release branch
git-release:
	git checkout -b release/$(VERSION)
	git add .
	git commit -m "release: $(VERSION)"
	git tag $(VERSION)
	git push origin release/$(VERSION)
	git push origin $(VERSION)