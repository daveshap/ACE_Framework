import asyncio
import re  # Import the re module here
from typing import TypedDict, Callable, Awaitable, Union


class MediaGenerator(TypedDict):
    keyword: str
    generator_function: Callable[[str], Awaitable[Union[str, None]]]


async def replace_media_prompt_with_media_url_formatted_as_markdown(media_generators: [MediaGenerator], message):
    for generator in media_generators:
        keyword = re.escape(generator['keyword'])  # Escape the keyword to ensure it's safe for regex
        pattern = re.compile(f"{keyword}\\[([^\\]]+)]")  # Create a regex pattern for this media generator

        matches = pattern.findall(message)
        coroutines = [generator['generator_function'](match) for match in matches]
        results = await asyncio.gather(*coroutines)

        for match, media_url in zip(matches, results):
            try:
                replacement = f"![{match}]({media_url})"
                message = message.replace(f"{generator['keyword']}[{match}]", replacement)
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    return message


async def split_message_by_media(media_generators: [MediaGenerator], message):
    segments = []
    last_end = 0  # Initialize last_end outside the loop
    for generator in media_generators:
        keyword = re.escape(generator['keyword'])
        pattern = re.compile(f"{keyword}\\[([^\\]]+)]")

        coroutines = []
        positions = []

        for match in pattern.finditer(message):
            media_prompt = match.group(1)
            text_segment = message[last_end:match.start()].strip()
            if text_segment:
                segments.append(text_segment)

            segments.append(None)
            coroutines.append(generator['generator_function'](media_prompt))
            positions.append(len(segments) - 1)

            last_end = match.end()  # Update last_end for each match

        results = await asyncio.gather(*coroutines)
        for result, position in zip(results, positions):
            try:
                segments[position] = result
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    final_text_segment = message[last_end:].strip()  # Move this line outside the loop
    if final_text_segment:  # Check and append final_text_segment outside the loop
        segments.append(final_text_segment)

    return segments

