#!/usr/bin/env bash
# Uploads the built site to S3 and refreshes CloudFront.
#   infra/deploy.sh            (uses the "hackathon" AWS profile; override with AWS_PROFILE=…)
# Only the public site goes up: index.html, the résumé PDF, images/, fonts/.
# Never build_src/, state.md, resume/, README.md, Fintrack/ or anything else in the repo.
set -euo pipefail
cd "$(dirname "$0")/.."

PROFILE="${AWS_PROFILE:-hackathon}"
REGION=ap-south-1
STACK=aryangorde-site
aws() { command aws --profile "$PROFILE" --region "$REGION" "$@"; }

# 1. The page must match its sources, and the public résumé must be the copy without the phone.
#    Matches any Indian mobile number (+91 optional, spaces/dashes allowed), so the number
#    itself never has to be written in this public repo.
python3 build.py --check
if pdftotext Aryan_Gorde_Resume.pdf - | grep -qE '(\+91[ -]?)?[6-9][0-9]{4}[ -]?[0-9]{5}'; then
  echo "ERROR: Aryan_Gorde_Resume.pdf has a phone number — run resume/build.sh" >&2; exit 1
fi

out() { aws cloudformation describe-stacks --stack-name "$STACK" \
          --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }
BUCKET=$(out BucketName)
DIST=$(out DistributionId)

# 2. Stage exactly the public files.
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT
cp index.html Aryan_Gorde_Resume.pdf "$stage"/
cp -r images fonts "$stage"/

# 3. Upload. Images and fonts cache for a week; the page and the PDF for five minutes.
#    --delete removes files from the bucket that are no longer part of the site.
aws s3 sync "$stage" "s3://$BUCKET" --delete --only-show-errors \
  --exclude "*" --include "images/*" --include "fonts/*" \
  --cache-control "public, max-age=604800"
aws s3 sync "$stage" "s3://$BUCKET" --delete --only-show-errors \
  --exclude "images/*" --exclude "fonts/*" \
  --cache-control "public, max-age=300"
# Re-put the page with an explicit charset (sync skips unchanged files, so do it every time).
aws s3 cp "$stage/index.html" "s3://$BUCKET/index.html" --only-show-errors \
  --content-type "text/html; charset=utf-8" --cache-control "public, max-age=300"

# 4. Clear CloudFront's copies so the new version shows everywhere at once.
id=$(aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/*" \
       --query Invalidation.Id --output text)
echo "deployed to s3://$BUCKET; CloudFront invalidation $id (live in ~1 minute)"
echo "https://$(out DistributionDomain)/"
