import boto3

# AWS constants
REGION = 'us-east-1'
BUCKET_NAME = 'speecher-bucket'

# Filenames
SOURCE_FILE = "source.txt"
TRANSLATED_FILE = "translated.txt"

def lambda_handler(event, context):
    text = read_file_from_bucket(SOURCE_FILE)
    source_language_code = "en"
    target_language_code = "de"
    
    print(f"Translating text from {source_language_code} to {target_language_code}...")
    translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True)
    translated_text = translate.translate_text(Text=text, 
                SourceLanguageCode=source_language_code, 
                TargetLanguageCode=target_language_code).get('TranslatedText')

    print('Uploading the translated file to the bucket...')
    write_file_to_bucket(TRANSLATED_FILE, translated_text)

    return "Success"
    

def read_file_from_bucket(filename):
    s3 = boto3.resource('s3')
    file_object = s3.Object(BUCKET_NAME, filename)
    content = file_object.get()['Body'].read().decode('utf-8')
    return content


def write_file_to_bucket(filename, content = None):
    if content is None:
        content = read_file(filename)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    with open('/tmp/output', "w") as data:
        data.write(content)

    bucket.upload_file('/tmp/output', filename)

