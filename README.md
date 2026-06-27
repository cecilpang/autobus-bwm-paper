## Paper: Business World Model

The AI agents use Google Gemini gemini-3.5-flash<br/>

### To run the demo:
1. Install uv: https://github.com/astral-sh/uv

2. Clone this repo and cd into the project directory.
    ```
    git clone https://github.com/cecilpang/autobus-bwm-paper.git
    cd autobus-bwm-paper
    ```

3. Place your Google Gemini API key in the file `.env` at the project directory. There should be one line in `.env`:
    ```
    GEMINI_API_KEY=<your Gemini key>
    ```

4. Generate churn reduction campaign</br>

    ```
    uv run --env-file .env --script src/churn_reduction_campaign.py
    ```