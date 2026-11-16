#!/usr/bin/env bash
# Uploads the built site to S3 and refreshes CloudFront.
#   infra/deploy.sh            (uses the "hackathon" AWS profile; override with AWS_PROFILE=…)
# GitHub Actions runs it too, on every push to main (.github/workflows/deploy.yml): there the
# credentials come from the environment (an OIDC role), so no profile is used.
# Only the public site goes up: the pages (index.html, 404.html, one folder per feature),
# the résumé PDF, images/, fonts/, video/ and og/.
# Never build_src/, state.md, resume/, README.md, Fintrack/ or anything else in the repo.
set -euo pipefail
cd "$(dirname "$0")/.."

REGION=ap-south-1
STACK=aryangorde-site
if [[ -n "${AWS_ACCESS_KEY_ID:-}" && -z "${AWS_PROFILE:-}" ]]; then
  aws() { command aws --region "$REGION" "$@"; }                      # CI: keys in the environment
else
  PROFILE="${AWS_PROFILE:-hackathon}"
  aws() { command aws --profile "$PROFILE" --region "$REGION" "$@"; }  # laptop: named profile
fi

# 1. The pages must match their sources, and the public résumé must be the copy without the phone.
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
pages=$(python3 -c "import sys; sys.path.insert(0, 'build_src'); sys.dont_write_bytecode = True; import content; print(' '.join(f['slug'] for f in content.FEATURES))")
cp index.html 404.html Aryan_Gorde_Resume.pdf "$stage"/
cp -r images fonts video og $pages "$stage"/

# 3. Upload. Images, fonts, loops and link previews cache for a week; the pages and the PDF
#    for five minutes. --delete removes files from the bucket that are no longer part of the site.
long=(--exclude "*" --include "images/*" --include "fonts/*" --include "video/*" --include "og/*")
aws s3 sync "$stage" "s3://$BUCKET" --delete --only-show-errors "${long[@]}" \
  --cache-control "public, max-age=604800"
aws s3 sync "$stage" "s3://$BUCKET" --delete --only-show-errors \
  --exclude "images/*" --exclude "fonts/*" --exclude "video/*" --exclude "og/*" \
  --cache-control "public, max-age=300"
# Re-put every page with an explicit charset (sync skips unchanged files, so do it every time).
for page in index.html 404.html $(for p in $pages; do echo "$p/index.html"; done); do
  aws s3 cp "$stage/$page" "s3://$BUCKET/$page" --only-show-errors \
    --content-type "text/html; charset=utf-8" --cache-control "public, max-age=300"
done

# 4. Clear CloudFront's copies so the new version shows everywhere at once.
id=$(aws cloudfront create-invalidation --distribution-id "$DIST" --paths "/*" \
       --query Invalidation.Id --output text)
echo "deployed to s3://$BUCKET; CloudFront invalidation $id (live in ~1 minute)"
echo "https://$(out DistributionDomain)/"
