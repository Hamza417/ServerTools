#!/usr/bin/env python3

import asyncio
import re
import sys
import xml.etree.ElementTree as ET

from googletrans import Translator
from tqdm.asyncio import tqdm_asyncio

FORMAT_PATTERN = re.compile(r'(%\d*\$?[sd])')
ESCAPE_PATTERN = re.compile(r'(\\n|\\t|\\")')


def protect_placeholders(text):
    placeholders = []

    def replacer(match):
        placeholders.append(match.group(0))
        return f"__PLACEHOLDER_{len(placeholders)}__"

    # First replace %1$s style
    text = FORMAT_PATTERN.sub(replacer, text)
    # Then \n, \t, \"
    text = ESCAPE_PATTERN.sub(replacer, text)

    return text, placeholders


def restore_placeholders(text, placeholders):
    for i, original in enumerate(placeholders, start=1):
        text = text.replace(f"__PLACEHOLDER_{i}__", original)
    return text


async def translate_text(translator, text, src_lang, dest_lang):
    try:
        safe_text, placeholders = protect_placeholders(text)
        translated = await translator.translate(safe_text, src=src_lang, dest=dest_lang)
        final_text = restore_placeholders(translated.text, placeholders)
        return final_text
    except Exception as e:
        print(f"⚠️ Error translating '{text}': {e}")
        return text


async def main():
    if len(sys.argv) != 5:
        print("Usage: python translate.py input.xml output.xml from_lang to_lang")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    src_lang = sys.argv[3]
    dest_lang = sys.argv[4]

    print(f"📄 Translating from {src_lang} ➝ {dest_lang}")
    print(f"🔍 Reading: {input_file}")

    tree = ET.parse(input_file)
    root = tree.getroot()

    translator = Translator()

    elements = []
    texts = []

    for elem in root.findall("string"):
        if elem.text:
            elements.append(elem)
            texts.append(elem.text)

    print(f"🚀 Translating {len(texts)} strings...\n")

    # Create a list of coroutines
    tasks = [translate_text(translator, text, src_lang, dest_lang) for text in texts]

    # Progress bar with asyncio.gather using tqdm_asyncio
    translated_texts = await tqdm_asyncio.gather(*tasks, desc="Progress")

    for elem, new_text in zip(elements, translated_texts):
        print(f"📝 {elem.attrib.get('name')}: {elem.text} ➝ {new_text}")
        elem.text = new_text

    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"\n✅ Translation complete ➝ {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
