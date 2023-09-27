# tools/image_tool.py
import re
import gpt


PATTERN = r"IMAGE\[([^\]]+)]"  # Regular expression pattern to find all occurrences of IMAGE[<prompt>]



def replace_image_prompt_with_image_url(message, markdown=False):
    """
    Replaces IMAGE[<prompt>] with a generated image URL.

    Args:
        message (str): The input message.
        markdown (bool, optional): Determines if the output should be in Markdown format. Defaults to False.

    Returns:
        str: The modified message with image URLs.
    """

    matches = re.findall(PATTERN, message)  # Find all matches of the pattern in the message.

    for match in matches:  # Loop through all the found matches.
        image_prompt = match  # Extract the prompt from the match.
        image_url = gpt.create_image(image_prompt)  # Generate the image URL using the create_image function.

        if markdown:  # Check if the format should be Markdown.
            replacement = f"![{image_prompt}]({image_url})"
        else:
            replacement = image_url + " \n"

        message = message.replace(f"IMAGE[{image_prompt}]", replacement)  # Replace the IMAGE[<prompt>] in the message.

    return message  # Return the modified message with image URLs.


def split_message_by_images(message):
    """
    Splits the message by IMAGE[<prompt>] and returns a list containing texts and image URLs.
    """

    segments = []  # List to store the segments of the message.
    last_end = 0  # The end of the last found IMAGE[<prompt>].
    for match in re.finditer(PATTERN, message):
        segments.append(message[last_end:match.start()])  # Append the text before the IMAGE[<prompt>].
        image_prompt = match.group(1)  # Extract the prompt from the match.
        image_url = gpt.create_image(image_prompt)  # Generate the image URL using the create_image function.
        segments.append(image_url)  # Append the generated image URL.
        last_end = match.end()  # Update the end of the last found IMAGE[<prompt>].

    segments.append(message[last_end:])  # Append the remaining text after the last IMAGE[<prompt>].
    return segments  # Return the list containing text and image URLs.


if __name__ == '__main__':
    test_message = "This is a test IMAGE[A painting of a cat sitting on a chair] and another IMAGE[A drawing of a sun]."
    print(replace_image_prompt_with_image_url(test_message, markdown=True))
