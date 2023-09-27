# tools/image_tool.py
import re
import gpt

def replace_image_prompt_with_image_url(message, markdown=False):
    """
    Replaces IMAGE[<prompt>] with a generated image URL.

    Args:
        message (str): The input message.
        markdown (bool, optional): Determines if the output should be in Markdown format. Defaults to False.

    Returns:
        str: The modified message with image URLs.
    """
    pattern = r"IMAGE\[([^\]]+)]"  # Regular expression pattern to find all occurrences of IMAGE[<prompt>]
    matches = re.findall(pattern, message)  # Find all matches of the pattern in the message.

    for match in matches:  # Loop through all the found matches.
        image_prompt = match  # Extract the prompt from the match.
        image_url = gpt.create_image(image_prompt)  # Generate the image URL using the create_image function.

        if markdown:  # Check if the format should be Markdown.
            replacement = f"![{image_prompt}]({image_url})"
        else:
            replacement = image_url + " \n"

        message = message.replace(f"IMAGE[{image_prompt}]", replacement)  # Replace the IMAGE[<prompt>] in the message.

    return message  # Return the modified message with image URLs.


if __name__ == '__main__':
    test_message = "This is a test IMAGE[A painting of a cat sitting on a chair] and another IMAGE[A drawing of a sun]."
    print(replace_image_prompt_with_image_url(test_message, markdown=True))
