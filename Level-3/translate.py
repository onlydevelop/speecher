#!/usr/bin/env python3

import boto3
import pygame

# AWS constants
REGION = 'us-east-1'
BUCKET_NAME = 'speecher-bucket'

# Constants
SOURCE_LANGUAGE_CODE = "en"
TARGET_LANGUAGE_CODE = "de"

# Filenames
SOURCE_FILE = "source.txt"
TRANSLATED_FILE = "translated.txt"
AUDIO_FILENAME = "speech.mp3"

def main():
    # The source text was generated from fairy tale generator:
    # https://www.plot-generator.org.uk/fairytale/
    print("Uploading the source file...")
    write_file_to_bucket(source_file)

    translate(SOURCE_FILE, SOURCE_LANGUAGE_CODE, TARGET_LANGUAGE_CODE)
    get_audio(AUDIO_FILENAME)
    play_audio(AUDIO_FILENAME)

def translate(source_file, source_language_code, target_language_code):
    print(f"Translating text from {souce_language_code} to {target_language_code}...")
    translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True)
    text = read_file(source_file)

    translated_text = translate.translate_text(Text=text,
                SourceLanguageCode=source_language_code,
                TargetLanguageCode=target_language_code).get('TranslatedText')

    print('Uploading the translated file to the bucket...')
    write_file_to_bucket(TRANSLATED_FILE, translated_text)


def get_audio(audio_filename):

    print("Getting the translated file from the bucket...")
    translated_text = read_file_from_bucket(TRANSLATED_FILE)
    print(translated_text)

    print("Generating audio file...")
    polly = boto3.client(service_name='polly', region_name=REGION, use_ssl=True)

    result = polly.synthesize_speech(VoiceId='Joanna',
            OutputFormat='mp3', 
            Text = translated_text)

    file = open(audio_filename, 'wb')
    file.write(result['AudioStream'].read())
    file.close()
    upload_file_to_bucket(audio_filename)


def play_audio(audio_filename):
    print(f"Playing audio {audio_filename}...")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
        pygame.time.Clock().tick(10)


def write_file_to_bucket(filename, content = None):
    if content is None:
        content = read_file(filename)

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    with open('/tmp/output', "w") as data:
        data.write(content)

    bucket.upload_file('/tmp/output', filename)

def upload_file_to_bucket(filename):
    content = open(filename, "rb").read()
    s3 = boto3.client(service_name='s3', region_name=REGION, use_ssl=True)
    s3.put_object(Body=content, Bucket=BUCKET_NAME, Key=filename)


def read_file_from_bucket(filename):
    s3 = boto3.resource('s3')
    file_object = s3.Object(BUCKET_NAME, filename)
    content = file_object.get()['Body'].read().decode('utf-8')
    return content


def read_file(filename):
    f = open(filename, "r")
    content = f.read()
    return content


if __name__ == '__main__':
    main()
