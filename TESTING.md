# Kubernetes Flask Application – Testing

This document records the tests performed while deploying a Python Flask application using Docker and Kubernetes.

## 1. Docker Image Testing

Built and tested the Flask application using Docker.

**Commands:**
```bash
docker build -t company-website:v1 .
docker run -d --name company-website-test -p 5000:5000 company-website:v1
```

**Results:**
- Flask website loaded at `http://localhost:5000`
- `/health` returned the application's healthy status
- `/info` returned application information

## 2. Kubernetes Deployment Testing

Deployed the application using `deployment.yaml`.

**Commands:**
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get deployments
kubectl get pods
```

**Results:**
- Deployment created successfully
- All 3 replicas reached Running and Ready status
- Health probes were configured for the application

## 3. Kubernetes Service Testing

Created a ClusterIP Service to access the Flask application.

**Commands:**
```bash
kubectl apply -f kubernetes/service.yaml
kubectl port-forward service/company-website-service 8080:80
```

**Results:**
- Website accessible at `http://localhost:8080`
- `/health` endpoint worked
- `/info` displayed the production environment

## 4. Horizontal Scaling

Tested increasing and decreasing the number of application replicas.

**Commands:**
```bash
kubectl scale deployment company-website --replicas=5
kubectl get pods

kubectl scale deployment company-website --replicas=2
kubectl get pods
```

**Results:**
- Initial replicas: 3
- Scaled up to 5 replicas successfully
- Scaled down to 2 replicas successfully

## 5. Kubernetes Self-Healing

Tested how Kubernetes handles the deletion of an application Pod.

**Commands:**
```bash
kubectl get pods
kubectl delete pod <pod-name>
kubectl get pods -w
```

**Results:**
- Deleted one running application Pod
- Kubernetes automatically created a replacement Pod
- Deployment returned to its desired state of 2 replicas

## 6. Application Logs and Troubleshooting

Inspected the running application's logs and container environment.

**Commands:**
```bash
kubectl logs deployment/company-website
kubectl describe pod <pod-name>
kubectl exec -it <pod-name> -- /bin/sh
```

**Results:**
- Successfully accessed Flask application logs
- Inspected Pod status, configuration and events
- Verified the `APP_ENV` environment variable was set to `production`

## 7. Rolling Update (v1 to v2)

Updated the Flask website heading and created a new Docker image.

**Commands:**
```bash
docker build -t company-website:v2 .
kubectl set image deployment/company-website company-website=company-website:v2
kubectl rollout status deployment/company-website
```

**Results:**
- Version 2 deployed successfully
- Deployment returned to Ready status
- Updated heading appeared in the browser

**Updated heading:**

`Welcome to Our Updated Company Website`

## 8. Application Rollback (v2 to v1)

Tested restoring the previous application version.

**Commands:**
```bash
kubectl rollout history deployment/company-website
kubectl rollout undo deployment/company-website
kubectl rollout status deployment/company-website
```

**Results:**
- Kubernetes restored the previous Deployment revision
- Application returned to version 1
- Original website heading appeared again

## 9. Issues Encountered

**Issue:** Kubernetes Pods initially failed with `ErrImageNeverPull`.

**Cause:** The Docker Desktop kind-based Kubernetes cluster could not access the locally built application image.

**Resolution:** Switched to the kubeadm-based Docker Desktop Kubernetes cluster, rebuilt the image, and deployed successfully.

**Lesson learned:** Container image availability depends on the Kubernetes cluster configuration. A Docker image existing locally does not always mean Kubernetes can access it.

## 10. Key Learnings

Through this lab, I learned how to:

- Containerize a Flask application using Docker
- Deploy and manage applications using Kubernetes
- Expose application Pods using a ClusterIP Service
- Scale application replicas
- Test Kubernetes self-healing
- Inspect application logs and troubleshoot problems
- Perform rolling updates and rollbacks
- Diagnose a container image availability issue