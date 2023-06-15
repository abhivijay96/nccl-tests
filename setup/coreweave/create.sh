#!/bin/bash

kubectl apply -f ssh-data-pvc.yaml
kubectl apply -f ssh-root-pvc.yaml
kubectl apply -f ssh-service.yaml
kubectl apply -f ssh-deployment.yaml