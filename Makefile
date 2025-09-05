IMAGE_NAMESPACE ?= okfn-brasil
IMAGE_NAME ?= querido-diario-backend
IMAGE_TAG ?= latest
IMAGE_FORMAT ?= docker

# Architecture detection and configuration
CURRENT_ARCH := $(shell uname -m)
ifeq ($(CURRENT_ARCH),x86_64)
    DEFAULT_PLATFORM := linux/amd64
else ifeq ($(CURRENT_ARCH),aarch64)
    DEFAULT_PLATFORM := linux/arm64
else ifeq ($(CURRENT_ARCH),arm64)
    DEFAULT_PLATFORM := linux/arm64
else
    DEFAULT_PLATFORM := linux/amd64
endif

# Allow override via command line flags
ifdef amd64
    PLATFORM := linux/amd64
else ifdef arm64
    PLATFORM := linux/arm64
else
    PLATFORM := $(DEFAULT_PLATFORM)
endif

.PHONY: build
build:
	cd app && docker build --platform $(PLATFORM) --tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: build-multi-arch
build-multi-arch:
	cd app && docker buildx build --platform linux/amd64,linux/arm64 --tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: login
login:
	docker login --username $(REGISTRY_USER) --password "$(REGISTRY_PASSWORD)" https://index.docker.io/v1/

.PHONY: publish
publish:
	docker tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):${IMAGE_TAG} $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(shell date --rfc-3339=date --utc)
	docker push $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(shell date --rfc-3339=date --utc)
	docker push $(IMAGE_NAMESPACE)/$(IMAGE_NAME):${IMAGE_TAG}

.PHONY: publish-tag
publish-tag:
	docker tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):${IMAGE_TAG} $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(shell git describe --tags)
	docker push $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(shell git describe --tags)

.PHONY: destroy
destroy:
	docker rmi --force $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: destroy-services
destroy-services:
	docker compose down --volumes --remove-orphans

.PHONY: create-services
create-services: destroy-services
	docker compose up -d postgres redis

.PHONY: test
test: create-services
	docker compose run --rm backend

.PHONY: shell
shell:
	docker compose run --rm backend bash

.PHONY: run
run: create-services
	docker compose up backend

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build           - Build image for current/specified architecture"
	@echo "  build-multi-arch - Build image for both amd64 and arm64 architectures"
	@echo "  publish         - Tag and push image with date and latest tags"
	@echo "  publish-tag     - Tag and push image with git tag"
	@echo "  destroy         - Remove local image"
	@echo "  help            - Show this help message"
	@echo ""
	@echo "Architecture flags:"
	@echo "  make build amd64=1    - Build for AMD64 architecture"
	@echo "  make build arm64=1    - Build for ARM64 architecture"
	@echo "  (default: auto-detect current architecture: $(DEFAULT_PLATFORM))"