import boto3

# AWS constants
REGION = 'us-east-1'
BUCKET_NAME = 'speecher-bucket'

# Filenames
TRANSLATED_FILE = "translated.txt"
AUDIO_FILENAME = "speech.mp3"

def lambda_handler(event, context):
    translated_text = read_file_from_bucket(TRANSLATED_FILE)
    polly = boto3.client(service_name='polly', region_name=REGION, use_ssl=True)
    
    result = polly.synthesize_speech(VoiceId='Joanna',
            OutputFormat='mp3', 
            Text = translated_text)

    file = open(f"/tmp/{AUDIO_FILENAME}", 'wb')
    file.write(result['AudioStream'].read())
    file.close()
    upload_file_to_bucket(AUDIO_FILENAME)
    
    return "Success"
    
def read_file_from_bucket(filename):
    s3 = boto3.resource('s3')
    file_object = s3.Object(BUCKET_NAME, f"translated/{filename}")
    content = file_object.get()['Body'].read().decode('utf-8')
    return content


def upload_file_to_bucket(filename):
    content = open(f"/tmp/{filename}", "rb").read()
    s3 = boto3.client(service_name='s3', region_name=REGION, use_ssl=True)
    s3.put_object(Body=content, Bucket=BUCKET_NAME, Key=f"speech/{filename}")
