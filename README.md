# Benchmarks for Chrontext
This repository contains the necessary resources to conduct benchmarks associated with Chrontext. These benchmarks are part of a forthcoming publication. 

## Overview
The benchmarks compare the performance of [Ontop VKG](https://ontop-vkg.org/) with [chrontext](https://github.com/magbak/chrontext). 
The benchmark scenario is a synthetically generated RDS (ISO/IEC 81346) model of a wind farm based on an example found [here](https://www.81346.com/s/RDS-PS-Wind-Farm-Example-hk82.pdf).
Additionally, we generate time series data which is associated with the model.
The benchmark is run on Kubernetes in Amazon Web Services (AWS). 

## AWS infrastructure setup
Set up the following on AWS.
- AWS Elastic Container Registries ([ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-console.html
)) named "dremio", "ontop" and "benchmark" used for custom images
- AWS S3 bucket for Dremio Storage
- AWS S3 bucket for time series data storage

