#!/usr/bin/env python3

import boto3

# AWS constants
REGION = 'us-east-1'

# Constants
SOURCE_LANGUAGE_CODE = "en"
TARGET_LANGUAGE_CODE = "de"

# Filenames
SOURCE_FILE = "source.txt"
TRANSLATED_FILE = "translated.txt"

def main():
    # The source text was generated from fairy tale generator:
    # https://www.plot-generator.org.uk/fairytale/
    translated_text = translate(SOURCE_FILE, SOURCE_LANGUAGE_CODE, TARGET_LANGUAGE_CODE)
    print(translated_text)
    

def translate(source_file, souce_language_code, target_language_code):
    print(f"Translating text from {souce_language_code} to {target_language_code}...")
    translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True)
    text = read_file(source_file)

    result = translate.translate_text(Text=text, 
                SourceLanguageCode=souce_language_code, 
                TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')


def read_file(filename):
    f = open(filename, "r")
    content = f.read()
    return content


if __name__ == '__main__':
    main()

