# LinguaFranka

Welcome to **LinguaFranka**, a language learning app that simulates conversations with a native speaker using state-of-the-art language models.

## Features

- **Simulated Conversations**: Chat with AI models like GPT-3.5, Gemini1.5-Pro, LLaMa2, and Claude 3 Haiku.
- **Profile Customization**: Create a personalized profile to enhance your learning experience.
- **Scenario Selection**: Choose specific scenarios for your conversations to match real-world situations.
- **Self-Hosted**: Run the app directly on your machine for privacy and control.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/StenzelK/LinguaFranka.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd LinguaFranka
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- **Start the Application**:
  - Use the provided batch script:
    ```bash
    start.bat
    ```
  - Alternatively, run manually with Uvicorn:
    ```bash
    uvicorn app:app --host 0.0.0.0 --port 8000
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
