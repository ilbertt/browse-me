# Browse Me

Use [Fabric](https://onfabric.io/) to browse the web on my behalf.

## Requirements

-   uv (https://docs.astral.sh/uv/)
-   An OpenAI API key (https://platform.openai.com/docs/api-reference)
-   A Fabric bearer token (obtain it from your browser session on Fabric)

## Usage

1. Install the dependencies:

    ```bash
    uv sync
    ```

2. Copy the `.env.example` file to `.env` and fill in the values.

3. Run the script:

    ```bash
    uv run main.py
    ```

You can change the prompt in the `main.py` file to suit your needs.
