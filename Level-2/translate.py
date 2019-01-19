#!/usr/bin/env python3

import boto3
import pygame

# AWS constants
REGION = 'us-east-1'

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
    translated_text = translate(SOURCE_FILE, SOURCE_LANGUAGE_CODE, TARGET_LANGUAGE_CODE)
    print(translated_text)
    get_audio(translated_text, AUDIO_FILENAME)
    play_audio(AUDIO_FILENAME)
    

def translate(source_file, souce_language_code, target_language_code):
    print(f"Translating text from {souce_language_code} to {target_language_code}...")
    translate = boto3.client(service_name='translate', region_name=REGION, use_ssl=True)
    text = read_file(source_file)

    result = translate.translate_text(Text=text, 
                SourceLanguageCode=souce_language_code, 
                TargetLanguageCode=target_language_code)
    return result.get('TranslatedText')


def get_audio(text, audio_filename):
    print(f"Downloading the translated audio file {audio_filename}...")
    polly = boto3.client(service_name='polly', region_name=REGION, use_ssl=True)
    result = polly.synthesize_speech(VoiceId='Joanna',
            OutputFormat='mp3', 
            Text = text)

    file = open(audio_filename, 'wb')
    file.write(result['AudioStream'].read())
    file.close()


def play_audio(audio_filename):
    print(f"Playing audio {audio_filename}...")
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): 
  
        pygame.time.Clock().tick(10)


def read_file(filename):
    f = open(filename, "r")
    content = f.read()
    return content


if __name__ == '__main__':
    main()

