# Kubernetes Flask Application — Testing and Validation

## Project overview

This document records the tests completed for **Lab 2: Deploying Your First Python Web Application on Kubernetes**, including the five additional exercises.

**Technologies:** Python, Flask, Docker, Docker Desktop, Kubernetes, kubectl, and YAML.

**Environment:** Local Docker Desktop Kubernetes cluster using kubeadm. Commands are run from the repository root unless a different directory is specified.

## 1. Docker image testing

Built and tested the initial Flask application locally.

```bash
docker build -t company-website:v1 .
docker run -d --name company-website-test -p 5000:5000 company-website:v1
```

**Results:** The website loaded at `http://localhost:5000`, `/health` reported a healthy application, and `/info` returned application information.

**Status:** Passed.

## 2. Kubernetes Deployment testing

Created a Deployment with three Flask replicas and HTTP readiness and liveness probes using `/health`.

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get deployments
kubectl get pods -l app=company-website
```

**Results:** Three Pods reached Running and Ready status (`3/3`).

**Status:** Passed.

## 3. Service and networking testing

Created a ClusterIP Service routing port 80 to Flask's container port 5000.

```bash
kubectl apply -f kubernetes/service.yaml
kubectl get services
kubectl port-forward service/company-website-service 8080:80
```

**Results:** The site was accessible at `http://localhost:8080`. The `/health` endpoint responded and `/info` reported the `production` environment.

**Status:** Passed.

## 4. Horizontal scaling

```bash
kubectl scale deployment company-website --replicas=5
kubectl get pods -l app=company-website
kubectl scale deployment company-website --replicas=2
kubectl get pods -l app=company-website
```

| Test | Ready replicas |
|---|---:|
| Initial Deployment | 3 |
| Scale up | 5 |
| Scale down | 2 |

**Results:** Kubernetes adjusted the number of Pods to match the requested replica count.

**Status:** Passed.

## 5. Initial self-healing test

After scaling to two replicas, deleted one application Pod and watched the Deployment recover.

```bash
kubectl get pods -l app=company-website
kubectl delete pod POD_NAME
kubectl get pods -l app=company-website -w
```

**Results:** Kubernetes created a replacement Pod, returning the Deployment to `2/2` Ready.

**Status:** Passed.

> `POD_NAME` in the commands is an example argument; use an actual Pod name from `kubectl get pods` when repeating the test.

## 6. Logs and container troubleshooting

```bash
kubectl logs deployment/company-website
kubectl describe pod POD_NAME
kubectl exec -it POD_NAME -- /bin/sh
```

Inside the container:

```sh
pwd
ls
printenv APP_ENV
exit
```

**Results:** Inspected Flask logs and Pod details, accessed a running container, and verified that `APP_ENV` was `production`.

**Status:** Passed.

## 7. Rolling update: v1 to v2

Changed the homepage heading to `Welcome to Our Updated Company Website`, rebuilt the image, and updated the Deployment.

```bash
docker build -t company-website:v2 .
kubectl set image deployment/company-website company-website=company-website:v2
kubectl rollout status deployment/company-website
kubectl get pods -l app=company-website
```

**Results:** Kubernetes rolled out v2 successfully, and the updated heading appeared in the browser.

**Status:** Passed.

## 8. Rollback: v2 to v1

```bash
kubectl rollout history deployment/company-website
kubectl rollout undo deployment/company-website
kubectl rollout status deployment/company-website
kubectl get deployment company-website -o jsonpath="{.spec.template.spec.containers[0].image}"
```

**Results:** The Deployment returned to `company-website:v1`, and the original homepage heading appeared again.

**Status:** Passed.

---

# Additional exercises

## Exercise 1 — Customize the company website

**Directory:** `exercises/1-customize-website/`

Created a separate Flask website for the fictional company **CloudTech Solutions** with a company name, address, contact email, services, application version `1.0`, and container hostname.

**Image:** `cloudtech-website:v1`  
**Deployment:** `cloudtech-website`  
**Replicas:** 2  
**Service:** `cloudtech-website-service`

From the Exercise 1 directory:

```bash
docker build -t cloudtech-website:v1 .
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl port-forward service/cloudtech-website-service 8081:80
```

**Results:** The custom image built successfully, both Pods became Ready, and the customized site loaded at `http://localhost:8081`.

**Status:** Passed.

## Exercise 2 — Deploy an Apache web server

**Directory:** `exercises/2-apache-server/`  
**Image:** `httpd:latest`  
**Deployment:** `apache-website`  
**Replicas:** 2  
**Container port:** 80  
**Service type:** ClusterIP

From the repository root:

```bash
kubectl apply -f exercises/2-apache-server/deployment.yaml
kubectl apply -f exercises/2-apache-server/service.yaml
kubectl get pods -l app=apache-website
kubectl port-forward service/apache-website-service 8082:80
```

**Results:** Both Apache Pods became Ready, and the default **It works!** page loaded at `http://localhost:8082`.

**Status:** Passed.

## Exercise 3 — Advanced application scaling

**Application:** `company-website`

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

| Operation | Requested replicas | Reported result |
|---|---:|---:|
| Initial | 2 | 2 |
| Scale up | 4 | 4 |
| Scale up | 6 | 6 |
| Scale down | 1 | 1 |

**Results:** Completed the required scaling sequence, increasing to six Pods and reducing to one.

**Status:** Passed, as reported during the lab.

## Exercise 4 — Kubernetes self-healing

**Application:** `company-website`

```bash
kubectl scale deployment company-website --replicas=3
kubectl get pods -l app=company-website
kubectl delete pod POD_NAME_1
kubectl get pods -l app=company-website -w
kubectl delete pod POD_NAME_2 POD_NAME_3
kubectl get pods -l app=company-website -w
```

| Test | Pods deleted | Final Ready replicas |
|---|---:|---:|
| Delete one Pod | 1 | 3/3 |
| Delete two Pods | 2 | 3/3 |

**Results:** Kubernetes created replacement Pods after each deletion test, restoring three Ready replicas.

**Status:** Passed.

> Pod names are dynamic. Replace `POD_NAME_1`, `POD_NAME_2`, and `POD_NAME_3` with currently running Pod names each time you repeat the demonstration.

## Exercise 5 – Deploy Nginx Using YAML

**Directory:** `exercises/5-yaml-deployment/`

**Objective:** Deploy an Nginx web application using Kubernetes YAML configuration files.

**Configuration:**
- Deployment: `student-website`
- Docker image: `nginx:latest`
- Replicas: 3
- Container port: 80
- Service type: ClusterIP

**Commands:**

```bash
kubectl apply -f exercises/5-yaml-deployment/deployment.yaml
kubectl apply -f exercises/5-yaml-deployment/service.yaml
kubectl get deployments
kubectl get pods -l app=student-website
kubectl port-forward service/student-website-service 8083:80
```

**Results:**
- Nginx Deployment created successfully
- All three Pods reached Ready status
- ClusterIP Service successfully exposed the Pods within Kubernetes
- Nginx welcome page accessible at `http://localhost:8083`

**Status:** Passed

**Key Learning:** Kubernetes YAML files can define application Deployments and Services without requiring manual Pod creation.

---

## Troubleshooting: `ErrImageNeverPull`

**Problem:** The initial Flask Deployment could not start its Pods because Kubernetes could not locate `company-website:v1` with `imagePullPolicy: Never`.

**Investigation:** Confirmed that the Docker image existed locally and that Docker Desktop was using a kind-based Kubernetes cluster. Its node image storage did not have the image required by the Deployment.

**Resolution:** Switched Docker Desktop Kubernetes to kubeadm, rebuilt the Docker image, and redeployed the Flask application. The Deployment then reached `3/3` Ready.

**Lesson learned:** An image available to the local Docker CLI is not necessarily available inside a Kubernetes node. Cluster configuration and container image storage matter when using local images.

## Key learnings

- Containerized a Flask application using Docker.
- Defined Kubernetes Deployments and ClusterIP Services using YAML.
- Accessed applications with `kubectl port-forward`.
- Scaled Deployments and observed automatic Pod replacement.
- Used logs, Pod descriptions, and container shells for troubleshooting.
- Performed a rolling update and rollback.
- Deployed Flask, Apache, and Nginx applications with separate Kubernetes resources.
- Investigated and resolved an image-availability problem.

## Demo screenshots

Screenshots have **not been captured yet**. During the planned demo, capture the Flask and customized websites, Apache and Nginx pages, Deployment/Pod readiness, Services, scaling output, self-healing, rolling update, and rollback. Add the relevant images to a `screenshots/` directory and link them from the repository README.

## Resource cleanup

The cluster resources are being retained for the demonstration. After the demo, they can be removed using their corresponding YAML files. Do not delete them before collecting screenshots.
