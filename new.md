# ---------------------------------------------
# AWS S3 CLI Setup – Prague Data
# This script includes explanations and commands
# for CLI access to the 'prague-data' bucket
# ---------------------------------------------

# 1️⃣ Install AWS CLI
# (Skip this step if already installed)
# Download from: https://aws.amazon.com/cli/
aws --version  # Verify installation

# 2️⃣ Configure AWS CLI profile for Prague user
# Replace <your-region> with your AWS region, e.g., us-east-1
aws configure --profile prague-user
# Enter when prompted:
# AWS Access Key ID: AKIAVPZUJKQGT7CIINMA
# AWS Secret Access Key: ZWGygSr90KtziF9AMJSXOQ1prNYxKF5S4ape5Whk
# Default region name: <your-region>
# Default output format: json

# 3️⃣ Test access to list files in the bucket
aws s3 ls s3://prague-data/ --profile prague-user

# 4️⃣ Upload a single file to the bucket
aws s3 cp "C:\path\to\file.txt" s3://prague-data/ --profile prague-user

# 5️⃣ Upload a folder recursively to the bucket
aws s3 cp "C:\path\to\folder" s3://prague-data/ --recursive --profile prague-user

# 6️⃣ Download a file from the bucket
aws s3 cp s3://prague-data/file.txt "C:\path\to\destination\" --profile prague-user

# Optional: Download a folder recursively from the bucket
aws s3 cp s3://prague-data/ "C:\path\to\destination\" --recursive --profile prague-user

# Notes:
# - The prague-user profile only has access to 'prague-data'.
# - Previous IAM profiles have been removed; this is the new dedicated user.
# - Keep your Access Key and Secret Key secure.
