# MCP Learning Project

A Model Context Protocol (MCP) server built as a learning project to understand and work with MCP. This server demonstrates how to create, deploy, and integrate MCP servers with various clients like Cursor.

## 🚀 Features

- **MCP Protocol Implementation**: Complete Model Context Protocol server
- **Tool Registration**: Demonstrates how to register and expose MCP tools
- **Health Monitoring**: Built-in health check endpoint for production monitoring
- **Cross-Platform Deployment**: Works locally and on AWS App Runner
- **Client Integration**: Ready for integration with Cursor and other MCP clients
- **Learning Examples**: Comprehensive examples of MCP patterns and best practices

## 🏗️ Architecture

- **Framework**: FastMCP (FastAPI-based MCP server)
- **Language**: Python 3.11
- **Data**: JSON-based sample database (toy data for learning)
- **Deployment**: Docker container with AWS App Runner support
- **Health Check**: `/health` endpoint for monitoring
- **MCP Version**: 2024-11-05 protocol

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)
- AWS CLI (for AWS deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mcp_games
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   python main.py
   ```

The server will be available at `http://localhost:8000`

## 🐳 Docker Deployment

### Build the Image
```bash
docker build -t mcp-laser-guns .
```

### Run Locally
```bash
docker run -p 8000:8000 mcp-laser-guns
```

### Cross-Platform Build (for AWS)
```bash
docker buildx build --platform linux/amd64 -t mcp-laser-guns:aws .
```

## ☁️ AWS App Runner Deployment

### Prerequisites
- AWS CLI configured
- ECR repository access

### Deploy to AWS

1. **Create ECR Repository**
   ```bash
   aws ecr create-repository --repository-name mcp-laser-guns --region us-east-2
   ```

2. **Login to ECR**
   ```bash
   aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-2.amazonaws.com
   ```

3. **Tag and Push**
   ```bash
   docker tag mcp-laser-guns:latest <account-id>.dkr.ecr.us-east-2.amazonaws.com/mcp-laser-guns:latest
   docker push <account-id>.dkr.ecr.us-east-2.amazonaws.com/mcp-laser-guns:latest
   ```

4. **Deploy to App Runner**
   - Use AWS Console or CLI to create App Runner service
   - Point to your ECR image
   - Configure health check at `/health`

## 🔧 Configuration

### Environment Variables
- `PORT`: Server port (default: 8000)
- `LASER_GUNS_FILE`: Path to laser guns JSON file (default: `laser_guns.json`)

### Health Check
The server provides a health check endpoint at `/health`:
```json
{
  "status": "healthy",
  "service": "acme-laser-guns-server",
  "version": "1.0.0"
}
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest -v
```

### Test Categories
- **Interface Tests** (19 tests): Core MCP tool functionality
- **Local Server Test** (1 test): Local deployment verification
- **MCP Client Test** (1 test): AWS App Runner deployment verification

### Test Coverage
- ✅ MCP protocol compliance
- ✅ Tool registration and execution
- ✅ Data loading and validation
- ✅ Search and filtering functionality
- ✅ Error handling
- ✅ Health check endpoints
- ✅ Cross-platform deployment

## 🔧 Available MCP Tools

### Core Tools
- `get_all_laser_guns`: Retrieve complete catalog (demonstrates data retrieval)
- `get_laser_gun_by_model`: Find specific model by name (demonstrates parameterized queries)
- `get_laser_guns_by_category`: Filter by category (demonstrates filtering)
- `get_laser_guns_by_price_range`: Filter by price range (demonstrates range queries)
- `get_random_laser_gun`: Get a random model (demonstrates random selection)
- `compare_laser_guns`: Compare two models side-by-side (demonstrates comparison logic)
- `get_acme_corp_info`: Company information (demonstrates metadata retrieval)

## 🌐 API Endpoints

### Health Check
- `GET /health` - Service health status

### MCP Protocol
- `POST /mcp/` - MCP protocol endpoint
- Supports initialization, tool calls, and session management

## 🔗 Integration

### Cursor MCP Configuration
Add to your Cursor MCP configuration (`~/.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "laser-guns": {
      "command": "npx",
      "args": ["-y", "mcp-http-bridge@latest"],
      "env": {
        "MCP_SERVER_URL": "https://q87vidpvch.us-east-2.awsapprunner.com/mcp/",
        "MCP_BRIDGE_DEBUG": "1"
      }
    }
  }
}
```

### Other MCP Clients
The server is compatible with any MCP client that supports HTTP-based MCP servers.

### Project Structure
```
mcp_games/
├── main.py                 # Server entry point
├── laser_gun_interface.py  # Core business logic (replace with your domain)
├── tool_registry.py        # MCP tool registration
├── laser_guns.json         # Sample data source (replace with your data)
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
├── tests/                  # Test suite
└── README.md              # This file
```

### Adding New MCP Tools
1. Add functionality to your interface file (e.g., `laser_gun_interface.py`)
2. Register new tools in `tool_registry.py`
3. Add tests in `tests/`
4. Update documentation

### Learning MCP Patterns
- **Tool Registration**: See how tools are registered in `tool_registry.py`
- **Parameter Handling**: Learn how to handle MCP tool parameters
- **Error Handling**: See how errors are handled and returned
- **Session Management**: Understand MCP session lifecycle

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Deployed at**: https://q87vidpvch.us-east-2.awsapprunner.com  
**Health Check**: https://q87vidpvch.us-east-2.awsapprunner.com/health  
