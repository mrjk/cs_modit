# The binary to build (just the basename).
MODULE := blueprint

# Where to push the docker image.
#REGISTRY ?= docker.pkg.github.com/mrjk/cs_modit
REGISTRY ?= mrjk/cs_modit

IMAGE := $(REGISTRY)/$(MODULE)

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)

build-dev:
	@echo "\n${BLUE}Building Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}\n"
	@sed                                 \
	    -e 's|{NAME}|$(MODULE)|g'        \
	    -e 's|{VERSION}|$(TAG)|g'        \
	    dev.Dockerfile | docker build -t $(IMAGE):$(TAG) -f- .

run-dev: build-dev
	@echo "\n${BLUE}Running Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}\n"
	@docker run -ti -v $(PWD)docker/etc:/app/etc -v $(PWD)docker/var:/app/var -p 4000 $(IMAGE):$(TAG)


build-prod:
	@echo "\n${BLUE}Building Production image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(VERSION)${NC}\n"
	@sed                                     \
	    -e 's|{NAME}|$(MODULE)|g'            \
	    -e 's|{VERSION}|$(VERSION)|g'        \
	    prod.Dockerfile | docker build -t $(IMAGE):$(VERSION) -f- .

# Example: make shell CMD="-c 'date > datefile'"
shell: build-dev
	@echo "\n${BLUE}Launching a shell in the containerized build environment...${NC}\n"
	  mkdir -p $(PWD)/tmp/etc $(PWD)/tmp/var
		docker run                                                     \
			-ti                                                     \
			--rm                                                    \
			--entrypoint /bin/bash                                  \
			-v $(PWD)/tmp/etc:/app/etc -v $(PWD)/tmp/var:/app/var -p 4000:4000   \
			-u $$(id -u):$$(id -g)                                  \
			$(IMAGE):$(TAG)						\
			$(CMD)

REGISTRY ?= docker.pkg.github.com/martinheinz/python-project-blueprint

push: build-prod
	@echo "\n${BLUE}Pushing image to GitHub Docker Registry...${NC}\n"
	@docker push $(IMAGE):$(VERSION)


docker-clean:
	@docker system prune -f --filter "label=name=$(MODULE)"


