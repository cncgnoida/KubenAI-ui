# AI Chat Assistant

A modern AI-powered chat interface built with Python and Streamlit, featuring flexible API support for both Azure OpenAI and local chat services.

## Features

- 🔄 **Dual API Support** 
  - Azure OpenAI integration for production use
  - Local Chat API support for development and testing
  - Easy switching between APIs via environment variables
- 🎯 **Configurable AI Behavior** 
  - Custom system messages to define AI personality and restrictions
  - Real-time system message updates
  - Conversation history management
- � **Developer-Friendly**
  - Docker support with host network access
  - Environment-based configuration
  - Clear logging and error handling
- 🎨 **Modern UI/UX**
  - Clean, responsive Streamlit interface
  - Real-time chat status indicators
  - Loading states and error handling
  - Customizable styling

![Chat UI Interface](docs/chat-ui-screenshot.png)

*The clean, modern interface showing the AI chat assistant in action with Azure OpenAI integration*

### Key UI Elements:
- **🟢 Connection Status**: Green indicator showing successful Azure OpenAI connection
- **💬 Chat Interface**: Clean message bubbles for user and AI responses  
- **🎯 Sidebar Controls**: Clear chat button and application information
- **⚡ Input Field**: "What's on your mind?" prompt for user queries
- **🤖 AI Responses**: Intelligent responses powered by Azure OpenAI

## Features

- 🤖 **AI-Powered Responses** - Integrated with Azure OpenAI for intelligent conversations
- 🎯 **Configurable AI Behavior** - Custom system messages to restrict AI to specific topics (e.g., Kubernetes-only)
- 💬 **Clean Chat Interface** - Modern, responsive design with message bubbles
- 📝 **Conversation History** - Maintains context throughout the chat session
- 🔒 **Secure Configuration** - Environment-based API key management
- ⚡ **Real-time Responses** - Fast, streaming-like experience with loading indicators
- 🎨 **Customizable UI** - Easy to modify styling and branding
- 🚀 **Quick Presets** - Pre-configured system messages for common use cases

## Prerequisites

- Docker (for containerized deployment)
- Python 3.11 or higher (for local development)
- Azure OpenAI resource with deployed model (if using Azure OpenAI)
- Local Chat API service (if using local API)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chat-ui.git
   cd chat-ui
   ```

2. Create your environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` with your configuration:
   - Set `CHAT_API_TYPE` to either 'azure' or 'local'
   - For Azure OpenAI: Configure the Azure-specific variables
   - For Local API: Set `LOCAL_CHAT_API_BASE_URL` (use host.docker.internal for Docker)

3. Build and run with Docker:
   ```bash
   # Build the image
   docker build -t chat-ui .

   # Run the container
   docker run -d \
     --name chat-ui-app \
     -p 8501:8501 \
     --add-host=host.docker.internal:host-gateway \
     --env-file .env \
     chat-ui
   ```

4. Access the UI at `http://localhost:8501`

### Option 2: Local Development

1. Clone and setup:
   ```bash
   git clone https://github.com/yourusername/chat-ui.git
   cd chat-ui
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Run the application:
   ```bash
   streamlit run src/main.py
   ```

## Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|----------|
| `CHAT_API_TYPE` | API to use ('azure' or 'local') | `azure` |
| `LOCAL_CHAT_API_BASE_URL` | Local Chat API URL | `http://localhost:8000` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | `your-api-key` |
| `AZURE_OPENAI_API_VERSION` | API version | `2025-01-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4` |

### Docker Network Configuration

When running with Docker:
- Use `host.docker.internal` to connect to services on the host machine
- Add `--add-host=host.docker.internal:host-gateway` for proper host resolution
- Map port 8501 for accessing the UI: `-p 8501:8501`

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Check if API type is correctly set in `.env`
   - Verify endpoint URLs and API keys
   - For local API, ensure host.docker.internal is properly configured

2. **Docker Network Issues**
   - Ensure the `--add-host` flag is included in docker run command
   - Check if local services are accessible from the container
   - Verify port mappings are correct

3. **Streamlit Interface**
   - Clear browser cache if UI changes aren't visible
   - Check container logs for any startup errors
   - Verify the application is running on the expected port
docker run -d \
  --name ai-chat-assistant \
  -p 8501:8501 \
  -e AZURE_OPENAI_ENDPOINT="your_endpoint_here" \
  -e AZURE_OPENAI_API_KEY="your_api_key_here" \
  -e AZURE_OPENAI_API_VERSION="2025-01-01-preview" \
  -e AZURE_OPENAI_DEPLOYMENT_NAME="your_deployment_name" \
  username/ai-chat-assistant:latest
```

#### Building from Source
1. **Clone the repository:**
```bash
git clone https://github.com/shubhasismathur/chat-ui.git
cd chat-ui
```

2. **Build and run with Docker:**
```bash
docker build -t ai-chat-assistant .
docker run -d -p 8501:8501 [environment variables] ai-chat-assistant
```

📖 **[Complete Container Deployment Guide](CONTAINER_GUIDE.md)**

### Option 2: Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/shubhasismathur/chat-ui.git
cd chat-ui
```

2. **Create a virtual environment:**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure Azure OpenAI:**
```bash
# Copy the example environment file
cp .env.example .env
# Edit .env with your Azure OpenAI credentials
```

5. **Set up your `.env` file with your Azure OpenAI credentials:**
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
# Optional: Custom system message for AI behavior
AZURE_OPENAI_SYSTEM_MESSAGE=You are a helpful AI assistant specialized in Kubernetes.
```

6. **Run the application:**
```bash
streamlit run src/main.py
```

7. **Open your browser and navigate to:** `http://localhost:8501`

## Configuration Options

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_API_VERSION` | API version to use | `2025-01-01-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your model deployment name | `gpt-4` or `gpt-35-turbo` |
| `AZURE_OPENAI_SYSTEM_MESSAGE` | Custom system message to define AI behavior | `You are an AI assistant specialized in Kubernetes...` |

### Supported Models

This application has been tested with:
- GPT-4 (recommended)
- GPT-3.5-turbo
- GPT-4o-mini

**Note:** Some models like `gpt-5-mini` may have parameter restrictions. The application automatically adjusts for model compatibility.

## 🎯 Customizing AI Behavior

### System Message Configuration

You can customize the AI's behavior and restrict it to specific topics using system messages. This allows you to create specialized chatbots (e.g., Kubernetes-only, Cloud computing, Programming assistance).

#### Method 1: Environment Variable
Set the `AZURE_OPENAI_SYSTEM_MESSAGE` in your `.env` file:

```env
# Example: Kubernetes-only assistant
AZURE_OPENAI_SYSTEM_MESSAGE=You are an AI assistant specialized in Kubernetes. Only answer questions related to Kubernetes, container orchestration, Docker, and cloud-native technologies. If asked about unrelated topics, politely redirect the conversation back to Kubernetes.

# Example: Cloud computing assistant
AZURE_OPENAI_SYSTEM_MESSAGE=You are an AI assistant specialized in cloud computing. Focus on topics related to AWS, Azure, Google Cloud, cloud architecture, DevOps, and infrastructure.
```

#### Method 2: Runtime Configuration
Use the sidebar in the application to:
- **Custom Text Area**: Write your own system message
- **Quick Presets**: Choose from pre-configured options:
  - 🤖 **General**: Standard helpful assistant
  - ☸️ **Kubernetes**: Kubernetes and container orchestration specialist
  - ☁️ **Cloud**: Cloud computing and DevOps expert
  - 💻 **Code**: Programming and development assistant

#### Example System Messages

```bash
# Kubernetes Specialist
"You are an AI assistant specialized in Kubernetes. Only answer questions related to Kubernetes, container orchestration, Docker, and cloud-native technologies."

# Security Expert
"You are a cybersecurity expert. Focus on security best practices, threat analysis, and protective measures. Always prioritize security in your recommendations."

# Code Reviewer
"You are a senior software engineer focused on code review. Analyze code for best practices, performance, security issues, and maintainability."
```

## Project Structure

```
chat-ui/
├── src/
│   ├── main.py                 # Main Streamlit application
│   ├── utils.py               # Utility functions for session management
│   └── azure_openai_service.py # Azure OpenAI integration service
├── docs/                      # Documentation and screenshots
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment configuration
├── .gitignore               # Git ignore rules
├── Dockerfile               # Container build configuration
├── .dockerignore           # Docker build exclusions
├── CONTAINER_GUIDE.md      # Complete containerization guide
└── README.md              # This file
```

## Usage

1. **Start a conversation** by typing in the chat input at the bottom
2. **View responses** from the AI assistant powered by Azure OpenAI
3. **Continue the conversation** - the app maintains context throughout the session
4. **Clear chat history** using the sidebar button
5. **Monitor connection status** via the sidebar indicator

## Troubleshooting

### Common Issues

**"Azure OpenAI Not Connected" in sidebar:**
- Check your `.env` file configuration
- Verify your Azure OpenAI endpoint and API key
- Ensure your deployment name matches exactly

**API Parameter Errors:**
- Some newer models have parameter restrictions
- The app automatically adjusts for most models
- Check Azure OpenAI documentation for your specific model

**Installation Issues:**
- Ensure Python 3.8+ is installed
- Try upgrading pip: `python -m pip install --upgrade pip`
- Use a fresh virtual environment if dependency conflicts occur

### Getting Help

- Check the [Azure OpenAI documentation](https://docs.microsoft.com/en-us/azure/cognitive-services/openai/)
- Review the application logs in the terminal
- Open an issue on GitHub if you encounter bugs

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

MIT