.PHONY: export_requirements deploy

all: deploy

export_requirements:
	poetry export -f requirements.txt -o requirements.txt

deploy: export_requirements
	gcloud functions deploy filter\
	  --source .\
	  --region=us-central1 \
	  --trigger-http \
	  --runtime python311 \
	  --allow-unauthenticated \
	  --entry-point filter_func \
	  --gen2 \
	  --memory 128Mi \
	  --service-account "sword-and-scale-filter-cloud-f@sword-and-scale-filter.iam.gserviceaccount.com" \
	  --max-instances 1 \
	  --set-secrets "SWORD_AND_SCALE_RSS_URL=SWORD_AND_SCALE_RSS_URL:1"
