# Kubernetes Deployment Testing

## Scaling Test

Tested horizontal scaling of the Flask `company-website` Deployment.

- Initial replicas: 3
- Scaled up to: 5
- Scaled down to: 2
- Verification commands: `kubectl get pods` and `kubectl get deployments`

## Self-Healing Test

Deleted one Pod managed by the Deployment and observed Kubernetes creating a replacement.

The Deployment returned to its desired replica count of two.

## Key Learning

Kubernetes Deployments manage the desired number of application replicas. When a managed Pod is deleted, the Deployment's ReplicaSet creates a replacement to restore the desired state.