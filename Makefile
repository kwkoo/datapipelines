IMAGE=ghcr.io/kwkoo/ocp-install
IMAGETAG=4.7

BASE:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: clusterinstall deploy create-transaction reset grafana kafdrop s3manager console image

clusterinstall:
	$(BASE)/scripts/run-install-job
	$(BASE)/scripts/install-camel-k

deploy:
	$(BASE)/scripts/install-ocs
	$(BASE)/scripts/install-amq-streams
	$(BASE)/scripts/install-serverless
	$(BASE)/scripts/configure-ocs
	$(BASE)/scripts/configure-knative-kafka
	$(BASE)/scripts/create-kafka-topics
	$(BASE)/scripts/install-kafdrop
	$(BASE)/scripts/install-db
	$(BASE)/scripts/configure-buckets
	$(BASE)/scripts/knative-services
	$(BASE)/scripts/install-grafana
	$(BASE)/scripts/install-s3manager
	$(BASE)/scripts/deploy-generator
	@rm -f /tmp/toolbox.json
	@echo "installation complete"

create-transaction:
	@oc apply -f $(BASE)/demos/ach/transaction-job.yaml

reset:
	@$(BASE)/scripts/reset-demo

grafana:
	@open https://`oc get -n ach route/grafana-route -o jsonpath='{.spec.host}'`

kafdrop:
	@open http://`oc get -n ach route/kafdrop -o jsonpath='{.spec.host}'`

s3manager:
	@open http://`oc get -n ach route/s3manager -o jsonpath='{.spec.host}'`

console:
	@open https://`oc get -n openshift-console route/console -o jsonpath='{.spec.host}'`

image:
	@docker build -t $(IMAGE):$(IMAGETAG) $(BASE)/install-image
	@docker push $(IMAGE):$(IMAGETAG)
	@docker tag $(IMAGE):$(IMAGETAG) $(IMAGE):latest
	@docker push $(IMAGE):latest
