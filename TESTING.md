# Kubernetes Flask Application – Testing and Validation

## Project Overview

This document records the testing performed for Lab 2: Deploying Your First Python Web Application on Kubernetes.

The project demonstrates how Docker and Kubernetes can be used to deploy, manage, scale, update, and troubleshoot containerized web applications.

**Technologies:** Python, Flask, Docker, Kubernetes, kubectl, YAML, and Docker Desktop.

---

## 1. Docker Image Testing

Built and tested the Flask application using Docker.

**Commands:**

```bash
docker build -t company-website:v1 .
docker run -d --name company-website-test -p 5000:5000 company-website:v1
```

**Results:**
- Flask website loaded at `http://localhost:5000`
- `/health` returned a healthy status
- `/info` returned application information

**Status:** Passed

## 2. Kubernetes Deployment Testing

Deployed the Flask application using a Kubernetes Deployment configured with three replicas.

**Commands:**

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get deployments
kubectl get pods
```

**Results:**
- Deployment created successfully
- All three replicas reached Ready status
- Readiness and liveness probes were configured using `/health`

**Status:** Passed

## 3. Kubernetes Service and Networking

Created a ClusterIP Service to provide a stable endpoint for the Flask application.

**Commands:**

```bash
kubectl apply -f kubernetes/service.yaml
kubectl get services
kubectl port-forward service/company-website-service 8080:80
```

**Results:**
- Website accessible at `http://localhost:8080`
- `/health` endpoint responded successfully
- `/info` displayed the production environment

**Status:** Passed

## 4. Horizontal Scaling

Tested increasing and decreasing the number of Flask application replicas.

**Commands:**

```bash
kubectl scale deployment company-website --replicas=5
kubectl get pods

kubectl scale deployment company-website --replicas=2
kubectl get pods
```

**Results:**

| Operation | Replicas |
|---|---:|
| Initial Deployment | 3 |
| Scale up | 5 |
| Scale down | 2 |

Kubernetes adjusted the number of application Pods to match the requested replica count.

**Status:** Passed

## 5. Kubernetes Self-Healing

Tested Kubernetes' ability to maintain the desired number of running Pods.

**Commands:**

```bash
kubectl get pods
kubectl delete pod <pod-name>
kubectl get pods -w
```

**Results:**
- Deleted one running application Pod
- Kubernetes automatically created a replacement Pod
- Deployment returned to the desired two replicas

**Status:** Passed

## 6. Application Logs and Troubleshooting

Inspected the running application's logs, Pod configuration, and container environment.

**Commands:**

```bash
kubectl logs deployment/company-website
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- /bin/sh
```

**Results:**
- Successfully viewed Flask application logs
- Inspected container configuration and Pod events
- Verified that `APP_ENV` was set to `production`

**Status:** Passed

## 7. Rolling Update – Version 1 to Version 2

Modified the Flask application heading and built a new Docker image.

**Commands:**

```bash
docker build -t company-website:v2 .
kubectl set image deployment/company-website company-website=company-website:v2
kubectl rollout status deployment/company-website
```

**Results:**
- Version 2 deployed successfully
- Deployment returned to Ready status
- Updated website heading appeared in the browser

**Updated heading:**

`Welcome to Our Updated Company Website`

**Status:** Passed

## 8. Application Rollback – Version 2 to Version 1

Tested restoring the previous application version using Kubernetes Deployment history.

**Commands:**

```bash
kubectl rollout history deployment/company-website
kubectl rollout undo deployment/company-website
kubectl rollout status deployment/company-website
```

**Results:**
- Kubernetes restored the previous Deployment revision
- The application returned to version 1
- The original website heading appeared again

**Status:** Passed

---

# Additional Lab Exercises

## Exercise 1 – Customize the Company Website

**Directory:** `exercises/1-customize-website/`

Created a customized Flask website for a fictional cloud services company, CloudTech Solutions.

**Implemented features:**
- Company name
- Fictional company address
- Contact email
- List of cloud services
- Application version 1.0
- Container hostname information

**Docker image:** `cloudtech-website:v1`

**Kubernetes Deployment:** `cloudtech-website`

**Replicas:** 2

**Commands:**

```bash
docker build -t cloudtech-website:v1 .
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl port-forward service/cloudtech-website-service 8081:80
```

The Kubernetes YAML commands above are run from the Exercise 1 directory.

**Results:**
- Customized Docker image built successfully
- Two Kubernetes Pods reached Ready status
- ClusterIP Service created successfully
- Website accessible at `http://localhost:8081`
- Company information and services displayed correctly

**Status:** Passed

## Exercise 2 – Deploy an Apache Web Server

**Directory:** `exercises/2-apache-server/`

Deployed an Apache HTTP Server using the official Docker image.

**Configuration:**
- Docker image: `httpd:latest`
- Deployment: `apache-website`
- Replicas: 2
- Container port: 80
- Service type: ClusterIP

**Commands:**

```bash
kubectl apply -f exercises/2-apache-server/deployment.yaml
kubectl apply -f exercises/2-apache-server/service.yaml
kubectl get deployments
kubectl get pods
kubectl port-forward service/apache-website-service 8082:80
```

**Results:**
- Apache Deployment created successfully
- Both replicas reached Ready status
- Kubernetes Service created successfully
- Apache default "It works!" page displayed at `http://localhost:8082`

**Status:** Passed

## Exercise 3 – Advanced Application Scaling

**Application:** `company-website`

**Objective:** Scale the existing Flask Deployment from 2 to 4 to 6 replicas, then reduce it to 1 replica.

**Commands:**

```bash
kubectl scale deployment company-website --replicas=2
kubectl get pods -l app=company-website

kubectl scale deployment company-website --replicas=4
kubectl get pods -l app=company-website

kubectl scale deployment company-website --replicas=6
kubectl get pods -l app=company-website

kubectl scale deployment company-website --replicas=1
kubectl get pods -l app=company-website
```
## Exercise 4 – Kubernetes Self-Healing

**Application:** `company-website`

**Objective:** Test Kubernetes' ability to maintain three replicas when application Pods are deleted.

**Commands:**

```bash
kubectl scale deployment company-website --replicas=3
kubectl get pods -l app=company-website

kubectl delete pod <pod-name>
kubectl get pods -l app=company-website -w

kubectl delete pod <pod-name-1> <pod-name-2>
kubectl get pods -l app=company-website -w
```

**Results:**

| Test | Pods Deleted | Final Ready Replicas |
|---|---:|---:|
| Single Pod failure | 1 | 3/3 |
| Multiple Pod failure | 2 | 3/3 |

Kubernetes automatically created replacement Pods to maintain the desired replica count.

**Status:** Passed

**Key Learning:** Kubernetes Deployments use ReplicaSets to maintain the desired number of Pods. When a managed Pod is deleted, a replacement is created automatically.

**Expected results:**

| Operation | Expected Ready Pods | Observed Pods |
|---|---:|---|
| Initial | 2 | To verify |
| Scale up | 4 | To verify |
| Scale up | 6 | To verify |
| Scale down | 1 | To verify |

**Status:** Pending verification

Once all four stages have been tested successfully, replace the observed values with your results and change the status to Passed.

---

## Troubleshooting – ErrImageNeverPull

**Issue:** Kubernetes initially failed to start the Flask application Pods with the `ErrImageNeverPull` error.

**Cause:** The Docker Desktop kind-based Kubernetes cluster could not access the locally built Docker image.

**Resolution:**
1. Confirmed the Docker image existed locally.
2. Investigated the Kubernetes cluster configuration.
3. Identified that Docker Desktop was using a kind-based cluster.
4. Switched to a kubeadm-based Docker Desktop cluster.
5. Rebuilt the Flask Docker image.
6. Redeployed the application successfully.

**Lesson learned:** Locally built Docker images are not necessarily available to every Kubernetes cluster. Image accessibility depends on the cluster's container runtime and image storage configuration.

---

## Key Learnings

Through this lab, I gained practical experience with:

- Building and running Python Flask applications in Docker
- Creating Kubernetes Deployments and Services using YAML
- Managing multiple replicas of containerized applications
- Accessing applications using Kubernetes port forwarding
- Scaling Deployments horizontally
- Testing Pod self-healing
- Inspecting logs and troubleshooting containers
- Performing rolling updates and rollbacks
- Deploying multiple independent web applications
- Troubleshooting Docker image availability in Kubernetes

## Screenshots and Demonstration

Screenshots will be captured during the final Kubernetes demonstration and added to the repository.

Planned evidence includes Deployment status, running websites, scaling results, Pod recovery, rolling updates, and rollback verification.