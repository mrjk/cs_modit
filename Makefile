# The binary to build (just the basename).
MODULE := build

# Where to push the docker image.
REGISTRY ?= mrjk/cs_modit
VENV_DIR ?= .venv

# Docker image namespace
IMAGE := $(REGISTRY)/$(MODULE)

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)


# Python Virtualenv management
# =====================================

$(VENV_DIR)/installed:
	@echo "\n${BLUE}Install Virtualenv locally:\n"
	test -d $(VENV_DIR) || virtualenv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate ; pip install -Ur requirements.txt
	touch $(VENV_DIR)/installed

run-venv: $(VENV_DIR)/installed
	@echo "\n${BLUE}Run Virtualenv code:\n"
	export FLASK_APP=app 
	export FLASK_ENV=development 
	@$(VENV_DIR)/bin/flask run


clean-venv:
	rm -rf venv
	find -iname "*.pyc" -delete


# Docker devel management
# =====================================

build-dev:
	@echo "\n${BLUE}Building Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}\n"
	@sed                                 \
	    -e 's|{NAME}|$(MODULE)|g'        \
	    -e 's|{VERSION}|$(TAG)|g'        \
	    dev.Dockerfile | docker build -t $(IMAGE):$(TAG) -f- .


run-dev: #build-dev
	@echo "\n${BLUE}Running Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}\n"
	mkdir -p $(PWD)/tmp/etc $(PWD)/tmp/var  $(PWD)/tmp/uploads
	docker run -ti --rm \
			-v $(PWD)docker/etc:/app/etc 	\
			-v $(PWD)docker/var:/app/var 	\
			-v $(PWD)docker/uploads:/app/uploads 	\
			-p 4000:4000 											\
			-u $$(id -u):$$(id -g)        \
			$(IMAGE):$(TAG)


# Docker production
# =====================================

build-prod:
	@echo "\n${BLUE}Building Production image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(VERSION)${NC}\n"
	@sed                                     \
	    -e 's|{NAME}|$(MODULE)|g'            \
	    -e 's|{VERSION}|$(VERSION)|g'        \
	    prod.Dockerfile | docker build -t $(IMAGE):$(VERSION) -f- .


push-prod: build-prod
	@echo "\n${BLUE}Pushing image to GitHub Docker Registry...${NC}\n"
	@docker push $(IMAGE):$(VERSION)


# Docker clean and debug
# =====================================

shell-dev: #build-dev
	@echo "\n${BLUE}Launching a shell in the containerized build environment...${NC}\n"
	mkdir -p $(PWD)/tmp/etc $(PWD)/tmp/var  $(PWD)/tmp/uploads
		docker run                                                     \
			-ti                                                     \
			--rm                                                    \
			--entrypoint /bin/bash                                  \
			-v $(PWD)/tmp/etc:/app/etc -v $(PWD)/tmp/var:/app/var -p 4000:4000   \
			-v $(PWD)docker/uploads:/app/uploads 	\
			-u $$(id -u):$$(id -g)                                  \
			$(IMAGE):$(TAG)						\
			$(CMD)


docker-clean:
	@docker system prune -f --filter "label=name=$(MODULE)"


