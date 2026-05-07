import boto3
from botocore.exceptions import NoCredentialsError

print("🚀 [SYSTEM]: Starting AWS S3 migration..." )

AWS_BUCKET_NAME ="gavi-enterprise-data-lake-2026"
LOCAL_FILE_PATH = "data/gold/gold_metrics.parquet"
S3_FILE_PATH = "ceo_dashboards/gold_metrics.parquet"

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"✅ [SUCCESS]: File '{local_file}' uploaded to S3 bucket '{bucket}' as '{s3_file}'.")
    except FileNotFoundError:
        print(f"❌ [ERROR]: The file '{local_file}' was not found.")
    except NoCredentialsError:
        print("❌ [ERROR]: AWS credentials not available.")
    except Exception as e:
        print(f"❌ [ERROR]: An error occurred: {e}")
upload_to_s3(LOCAL_FILE_PATH, AWS_BUCKET_NAME, S3_FILE_PATH)