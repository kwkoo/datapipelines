BASE:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

.PHONY: deploy create-transaction reset grafana kafdrop

deploy:
	@$(BASE)/scripts/install-ocs
	@$(BASE)/scripts/install-amq-streams
	@$(BASE)/scripts/install-serverless
	@$(BASE)/scripts/configure-ocs
	@$(BASE)/scripts/configure-knative-kafka
	@$(BASE)/scripts/create-kafka-topics
	@$(BASE)/scripts/install-kafdrop
	@$(BASE)/scripts/install-db
	@$(BASE)/scripts/configure-buckets
	@$(BASE)/scripts/knative-services
	@$(BASE)/scripts/install-grafana
	@echo "installation complete"

create-transaction:
	@oc apply -f $(BASE)/demos/ach/transaction-job.yaml

reset:
	@$(BASE)/scripts/reset-demo

grafana:
	@open https://`oc get -n ach route/grafana-route -o jsonpath='{.spec.host}'`

kafdrop:
	@open http://`oc get -n ach route/kafdrop -o jsonpath='{.spec.host}'`
