import pytest

from media.media_replace import replace_media_prompt_with_media_url_formatted_as_markdown, split_message_by_media


# Simulated media generator functions
async def fake_image_generator(prompt: str) -> str:
    return f"https://fake.image.url/{prompt}.jpg"


async def fake_gif_generator(prompt: str) -> str:
    return f"https://fake.gif.url/{prompt}.gif"

# Media generators
media_generators = [
    {"keyword": "IMAGE", "generator_function": fake_image_generator},
    {"keyword": "GIF", "generator_function": fake_gif_generator}
]


@pytest.mark.asyncio
async def test_replace_media_prompt_with_media_url_formatted_as_markdown():
    message = "Here's a fake IMAGE[cat] and a fake GIF[dance]."
    expected_result = "Here's a fake ![cat](https://fake.image.url/cat.jpg) and a fake ![dance](https://fake.gif.url/dance.gif)."
    result = await replace_media_prompt_with_media_url_formatted_as_markdown(media_generators, message)
    assert result == expected_result


@pytest.mark.asyncio
async def test_split_message_by_media_no_media():
    message = "This is a test message with no media."
    expected_output = ["This is a test message with no media."]  # Expected output is a list with the original message

    output = await split_message_by_media(media_generators, message)
    assert output == expected_output, f"expected {expected_output} but got {output}"


@pytest.mark.asyncio
async def test_split_message_by_media():
    message = "Here's a fake IMAGE[cat] and a fake GIF[dance]."
    expected_result = ["Here's a fake", "https://fake.image.url/cat.jpg", "and a fake", "https://fake.gif.url/dance.gif", "."]
    result = await split_message_by_media(media_generators, message)
    assert result == expected_result

if __name__ == '__main__':
    pytest.main([__file__])
