from loguru import logger
from openai import OpenAI
import os
import random
import requests

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def read_api_key(file_path):
    """
    Read the API key from a file.

    :param file_path: Path to the file containing the API key
    :return: API key as a string
    """
    try:
        # Ensure the file exists
        if not os.path.exists(file_path):
            logger.critical(f"The file {file_path} does not exist.")
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Open the file and read the API key
        with open(file_path, "r") as file:
            api_key = file.read().strip()

        # Check if the API key is empty
        if not api_key:
            logger.critical("The API key file is empty.")
            raise ValueError("The API key file is empty.")

        return api_key

    except Exception as e:
        logger.critical(f"An error occurred while reading the API key: {str(e)}")
        return None


def get_random_topic():
    topics = [
        "architecture",
        "art",
        "attitude",
        "business",
        "change",
        "communication",
        "courage",
        "dreams",
        "education",
        "environment",
        "equality",
        "failure",
        "family",
        "fear",
        "forgiveness",
        "friendship",
        "happiness",
        "health",
        "hope",
        "inspiration",
        "knowledge",
        "leadership",
        "learning",
        "life",
        "love",
        "success",
    ]

    chosen_topic = random.choice(topics)
    logger.info(f"Topic chosen: {chosen_topic}")
    return chosen_topic


def get_inspirational_quote(perplexity_api_key):
    try:
        topic = get_random_topic()
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {
                    "content": f"Generate quote about {topic}. Generate one for me, don't give me instructions to get one.",
                    "role": "user",
                }
            ],
            # Temperature helps with randomness. Otherwise we keep getting the same quote
            "temperature": 1,
        }

        headers = {
            "Authorization": f"Bearer {perplexity_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST", PERPLEXITY_API_URL, json=payload, headers=headers
        ).json()
        logger.info(f"Perplexity response: {response}")

        choices = response.get("choices", [])
        quote = choices[0].get("message").get("content")

        logger.info(f"Generated quote: {quote}")
        return quote
    except Exception as e:
        logger.critical(
            f"An error occurred while generating inspirational quote: {str(e)}"
        )
        return None


def generate_image(openai_api_key, quote):
    try:
        client = OpenAI(api_key=openai_api_key)

        images = client.images.generate(
            model="dall-e-3",
            prompt=f"Visualize this quote but do not include the quote in the image - {quote}",
            n=1,
            size="1024x1024",
            style="natural",
        ).data
        logger.info(f"OpenAI response: {images}")

        image_urls = [item.url for item in images]
        revised_prompts = [item.revised_prompt for item in images]

        logger.info(f"Revised prompts: {revised_prompts}")
        logger.info(f"Image URLs: {image_urls}")
        return image_urls

    except Exception as e:
        logger.critical(f"An error occurred while generating Dall-E image: {str(e)}")
        return None


def main():
    # Read perplexity API key
    perplexity_api_key_file = "secrets/perplexity_api_key"
    perplexity_api_key = read_api_key(perplexity_api_key_file)

    # Read openAI API key
    openai_api_key_file = "secrets/openai_api_key"
    openai_api_key = read_api_key(openai_api_key_file)

    if not perplexity_api_key:
        logger.error("Failed to read Perplexity API key.")
        os.exit(1)

    if not openai_api_key:
        logger.error("Failed to read Perplexity API key.")
        os.exit(1)

    logger.info("Perplexity API key successfully read.")
    logger.info("OpenAI API key successfully read.")
    quote = get_inspirational_quote(perplexity_api_key)

    generate_image(openai_api_key, quote)


if __name__ == "__main__":
    main()
