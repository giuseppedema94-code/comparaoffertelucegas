#!/bin/bash
# Collega GitHub Actions (repo comparaoffertelucegas) all'account di servizio report-siti, senza chiavi.
# Da lanciare una volta in Cloud Shell del progetto comparaofferte. File temporaneo: verra rimosso.
P=comparaofferte
N=$(gcloud projects describe $P --format='value(projectNumber)')
SA=report-siti@$P.iam.gserviceaccount.com
REPO=giuseppedema94-code/comparaoffertelucegas
gcloud iam workload-identity-pools create github --project=$P --location=global --display-name=GitHub --quiet
gcloud iam workload-identity-pools providers create-oidc github --project=$P --location=global \
  --workload-identity-pool=github --issuer-uri=https://token.actions.githubusercontent.com \
  --attribute-mapping=google.subject=assertion.sub,attribute.repository=assertion.repository \
  --attribute-condition="assertion.repository=='$REPO'" --quiet
gcloud iam service-accounts add-iam-policy-binding $SA --project=$P --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$N/locations/global/workloadIdentityPools/github/attribute.repository/$REPO" \
  --quiet --format='value(etag)'
echo "PROVIDER=projects/$N/locations/global/workloadIdentityPools/github/providers/github"
echo FATTO
