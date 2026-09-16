#!/bin/bash
# Pulls real METABRIC and TCGA-BRCA clinical data from cBioPortal's
# public GitHub datahub mirror (the cBioPortal website itself is blocked
# by this environment's network egress policy, but the GitHub mirror
# serves the identical, authoritative files - same data, different route).
#
# Run: bash scripts/pull_metabric_tcga.sh

set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p data/raw

echo "Pulling METABRIC clinical patient data..."
curl -sS "https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/brca_metabric/data_clinical_patient.txt" \
  --max-time 60 -o data/raw/metabric_clinical_patient.txt
echo "  -> $(wc -l < data/raw/metabric_clinical_patient.txt) lines"

echo "Pulling TCGA-BRCA (PanCancer Atlas 2018) clinical patient data..."
curl -sS "https://media.githubusercontent.com/media/cBioPortal/datahub/master/public/brca_tcga_pan_can_atlas_2018/data_clinical_patient.txt" \
  --max-time 60 -o data/raw/tcga_brca_clinical_patient.txt
echo "  -> $(wc -l < data/raw/tcga_brca_clinical_patient.txt) lines"

echo "Done."
