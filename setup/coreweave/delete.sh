#!/bin/bash

kubectl delete -f ssh-data-pvc.yaml
kubectl delete -f ssh-root-pvc.yaml
kubectl delete -f ssh-service.yaml
kubectl delete -f ssh-deployment.yaml