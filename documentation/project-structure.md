# Project Structure

This project is structured as a Jupyter Notebook-based implementation, designed to run code blocks sequentially through an agent system. The following technical specifications outline the project's architecture and requirements:

## Environment & Dependencies
- Python 3.12
- Package Management: Dependencies are installed via pip within the Jupyter Notebook environment

## Implementation Approach
- Single Jupyter Notebook Implementation
  - No separate agent files
  - No standalone API interaction files
  - All code execution happens within notebook cells
  - Sequential code block execution through the agent system

## Technical Details
- Package Installation: All required packages are installed directly into the virtual environment through pip commands executed in notebook cells
- API Integration: API interactions are handled within the notebook environment
- Agent System: Implemented as notebook cells rather than separate Python modules

## Configuration Variables (`config.json`) and Notebook Settings

The project uses a combination of configuration variables stored in `config.json` and settings that can be safely set directly in the Jupyter notebook. This separation helps maintain security for sensitive information while allowing flexibility for experimentation and debugging.

### Variables to Keep in `config.json` (Sensitive or Environment-Specific)
These variables should **not** be hardcoded in the notebook and must remain in `config.json`:

- **openai_api_key**: API key for OpenAI (sensitive)
- **langfuse_secret**: Secret key for Langfuse (sensitive)
- **langfuse_public_key**: Public key for Langfuse (should be kept in config)
- **host**: Base URL for Langfuse tracing service (environment-specific)
- **HF_TOKEN**: Hugging Face token (sensitive)

**Best Practice:**
- Only keep sensitive keys and environment-specific endpoints in `config.json`.
- Use the notebook for settings that are safe to share, experiment with, or override during development.

This structure serves as a reference document for technical implementation details and can be consulted when making modifications to the project.
