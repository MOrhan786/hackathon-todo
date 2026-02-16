#!/bin/bash
# Oracle Cloud OKE Cluster Setup Script
# Prerequisites: OCI CLI configured, kubectl installed, Helm 3 installed
#
# Usage: ./scripts/oke-setup.sh
# Environment variables:
#   OKE_CLUSTER_ID  - OKE cluster OCID
#   COMPARTMENT_ID  - Compartment OCID
#   REGION          - OCI region (e.g., us-ashburn-1)

set -euo pipefail

NAMESPACE="todo-app"
DAPR_VERSION="1.13"

echo "=== Oracle Cloud OKE Setup ==="

# Step 1: Configure kubectl for OKE cluster
echo ""
echo "--- Step 1: Configuring kubectl ---"
if [ -z "${OKE_CLUSTER_ID:-}" ]; then
  echo "ERROR: OKE_CLUSTER_ID environment variable is required."
  echo "  export OKE_CLUSTER_ID=ocid1.cluster.oc1..."
  exit 1
fi

oci ce cluster create-kubeconfig \
  --cluster-id "$OKE_CLUSTER_ID" \
  --file "$HOME/.kube/config" \
  --region "${REGION:-us-ashburn-1}" \
  --token-version 2.0.0 \
  --kube-endpoint PUBLIC_ENDPOINT

echo "kubectl configured for OKE cluster."
kubectl cluster-info

# Step 2: Create namespace
echo ""
echo "--- Step 2: Creating namespace ---"
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
echo "Namespace '$NAMESPACE' ready."

# Step 3: Install Dapr
echo ""
echo "--- Step 3: Installing Dapr ---"
if ! command -v dapr &> /dev/null; then
  echo "Installing Dapr CLI..."
  wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.sh -O - | /bin/bash
fi

dapr init --kubernetes --runtime-version "$DAPR_VERSION" --wait
echo "Dapr installed and initialized on cluster."

# Step 4: Verify Dapr
echo ""
echo "--- Step 4: Verifying Dapr ---"
dapr status -k
kubectl get pods -n dapr-system

# Step 5: Create OCIR pull secret (if needed)
echo ""
echo "--- Step 5: OCIR Pull Secret ---"
if [ -n "${OCIR_USERNAME:-}" ] && [ -n "${OCIR_TOKEN:-}" ] && [ -n "${OCIR_REGISTRY:-}" ]; then
  kubectl create secret docker-registry ocir-secret \
    --namespace "$NAMESPACE" \
    --docker-server="$OCIR_REGISTRY" \
    --docker-username="$OCIR_USERNAME" \
    --docker-password="$OCIR_TOKEN" \
    --docker-email="${OCIR_EMAIL:-noreply@example.com}" \
    --dry-run=client -o yaml | kubectl apply -f -
  echo "OCIR pull secret created."
else
  echo "OCIR credentials not set. Skipping pull secret creation."
  echo "  Set OCIR_REGISTRY, OCIR_USERNAME, OCIR_TOKEN to create pull secret."
fi

echo ""
echo "=== OKE Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Build and push images: ./scripts/push-images.sh"
echo "  2. Deploy with Helm:"
echo "     helm install todo-app ./helm/todo-app/ \\"
echo "       -f helm/todo-app/values-oke.yaml \\"
echo "       -f values-secrets.yaml \\"
echo "       --namespace $NAMESPACE"
