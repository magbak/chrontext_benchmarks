# Benchmarks for Chrontext
This repository contains the necessary resources to conduct benchmarks associated with Chrontext. These benchmarks are part of a forthcoming publication. 

## Overview
The benchmarks compare the performance of [Ontop VKG](https://ontop-vkg.org/) with [chrontext](https://github.com/magbak/chrontext). 
The benchmark scenario is a synthetically generated RDS (ISO/IEC 81346) model of a wind farm based on an example found [here](https://www.81346.com/s/RDS-PS-Wind-Farm-Example-hk82.pdf).
Additionally, we generate time series data which is associated with the model.
The benchmark is run on Kubernetes in Amazon Web Services (AWS). 

## Creating test data locally
- Install maplib locally from [here](https://github.com/magbak/maplib)
- Install jupyter notebook locally (e.g. pip install jupyter notebook)
- Start jupyter notebook and run all cells in mapping.ipynb
- Run all cells in timeseries_energy_production.ipynb, timeseries_wind_direction.ipynb and timeseries_wind_speed.ipynb
- Run the script rewrite_dataset_paths.py

## AWS infrastructure setup
- AWS Elastic Container Registries ([ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-console.html
)) named "dremio", "ontop" and "benchmark" used for custom images
- AWS S3 bucket for Dremio Storage
- AWS S3 bucket for time series data storage, we have assumed chrontext-benchmark
- Place chrontext wheel in benchmark-docker folder (find it [here](https://github.com/magbak/chrontext))
- Update Dockerfile in same folder to be consistent (two places!)
- Fill in AWS account id in aws_docker_build_tag.sh
- Fill in AWS account id in 03-ontop.yaml
- Fill in user/password for Dremio in benchmark_chrontext.py
- Fill in user/password for Dremio in 03-ontop.yaml
- Install and log into aws cli
- Login docker to ECR (replace ID_HERE with account id): aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ID_HERE.dkr.ecr.eu-west-2.amazonaws.com
- Run ./aws_docker_build_tag.sh
- Clone and configure the [Dremio Helm Chart](https://github.com/dremio/dremio-cloud-tools/tree/master/charts/dremio_v2) - remember bucket for Dremio Storage
- Create an AMS EKS cluster and create a node group with enough nodes for Dremio (1+3+3), Postgres (+1), Ontop(+1) and the Benchmark container (+1)
- Install kubectl locally
- Configure kubectl: aws eks update-kubeconfig --region eu-west-2 --name chrontext-cluster
- Deploy Dremio to this EKS cluster using Helm (e.g. in the charts-folder: helm install dremio-release dremio_v2 -f dremio_v2/values.yaml
- Note that we will need +3 nodes for zookeeper
- Navigate to the kubernetes folder to deploy postgres
- kubectl apply -f 00-namespace.yaml
- kubectl config set-context --current --namespace=chrontext
- kubectl apply -f 01-postgresql.yaml
- Find the dremio address using kubectl get all -A Put it into a browser and add :9047 
- Log in and set up s3 (name:s3) and postgres (name:postgres, postgres-0.postgres.chrontext.svc.cluster.local) data sources (check 00-postgresql.yaml for user/pass)
- Navigate to the s3 data source and format the timeseries_boolean, timeseries_double folders
- kubectl apply -f 02-ontop.yaml
- Fill in account id in the kubernetes/benchmark-node.yaml
- kubectl apply -f 03-benchmark-node.yaml
- kubectl exec --stdin --tty benchmark-0 -- /bin/bash
- source .venv/bin/activate
- python benchmark_chrontext.py
- python benchmark_ontop.py