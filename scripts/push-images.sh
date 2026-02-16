#!/bin/bash
# Build and push Docker images to Oracle Cloud OCIR
#
# Usage: ./scripts/push-images.sh
# Environment variables (required):
#   OCIR_REGISTRY      - e.g., us-ashburn-1.ocir.io
#   OCIR_NAMESPACE      - Tenancy namespace
#   IMAGE_TAG           - Image tag (default: latest)

set -euo pipefail

if [ -z "${OCIR_REGISTRY:-}" ] || [ -z "${OCIR_NAMESPACE:-}" ]; then
  echo "ERROR: OCIR_REGISTRY and OCIR_NAMESPACE are required."
  echo "  export OCIR_REGISTRY=<region>.ocir.io"
  echo "  export OCIR_NAMESPACE=<tenancy-namespace>"
  exit 1
fi

TAG="${IMAGE_TAG:-latest}"
REPO_PREFIX="${OCIR_REGISTRY}/${OCIR_NAMESPACE}/todo-app"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== Building and Pushing Docker Images ==="
echo "Registry: $REPO_PREFIX"
echo "Tag: $TAG"
echo ""

# Login to OCIR
echo "--- Logging in to OCIR ---"
if [ -n "${OCIR_TOKEN:-}" ] && [ -n "${OCIR_USERNAME:-}" ]; then
  echo "$OCIR_TOKEN" | docker login "$OCIR_REGISTRY" -u "${OCIR_NAMESPACE}/${OCIR_USERNAME}" --password-stdin
else
  echo "OCIR_TOKEN and OCIR_USERNAME not set. Assuming already logged in."
fi

# Build and push backend
echo ""
echo "--- Building backend ---"
docker build \
  -t "${REPO_PREFIX}/backend:${TAG}" \
  -f "${PROJECT_ROOT}/backend/Dockerfile" \
  "${PROJECT_ROOT}/backend"

echo "--- Pushing backend ---"
docker push "${REPO_PREFIX}/backend:${TAG}"

# Build and push frontend
echo ""
echo "--- Building frontend ---"
docker build \
  -t "${REPO_PREFIX}/frontend:${TAG}" \
  -f "${PROJECT_ROOT}/frontend/Dockerfile" \
  --build-arg NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://localhost:8000}" \
  "${PROJECT_ROOT}/frontend"

echo "--- Pushing frontend ---"
docker push "${REPO_PREFIX}/frontend:${TAG}"

# Build and push notification consumer
echo ""
echo "--- Building notification-consumer ---"
docker build \
  -t "${REPO_PREFIX}/notification-consumer:${TAG}" \
  -f "${PROJECT_ROOT}/backend/consumers/Dockerfile" \
  "${PROJECT_ROOT}"

echo "--- Pushing notification-consumer ---"
docker push "${REPO_PREFIX}/notification-consumer:${TAG}"

echo ""
echo "=== All images pushed successfully ==="
echo ""
echo "Images:"
echo "  ${REPO_PREFIX}/backend:${TAG}"
echo "  ${REPO_PREFIX}/frontend:${TAG}"
echo "  ${REPO_PREFIX}/notification-consumer:${TAG}"
