# Authenex - Certificate Verification System

A comprehensive certificate verification system combining AI-powered document analysis with blockchain technology.

## 🏗️ Architecture

- **FastAPI Backend**: AI-powered certificate parsing, photo/signature verification, blockchain integration
- **React Frontend**: Modern web interface for certificate verification and management
- **Blockchain**: Smart contract-based certificate storage and verification

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd Authenex/Backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start the server**
   ```bash
   python start.py
   ```
   
   Or directly:
   ```bash
   python main.py
   ```

   API will be available at: http://localhost:8000
   Documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd Authenex/Frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at: http://localhost:5173

## 📋 Features

### ✅ Working Features
- **Certificate Parsing**: Upload certificate images for AI-powered data extraction
- **Blockchain Storage**: Store certificate data on blockchain with hash verification
- **Certificate Verification**: Verify certificates by hash lookup
- **Photo Verification**: Face matching between photos (mock/real AI)
- **Signature Verification**: Signature comparison (mock/real AI)
- **Health Monitoring**: System status dashboard
- **Responsive UI**: Modern React interface

### 🔧 API Endpoints

- `GET /health` - System health check
- `POST /parse-certificate/` - Parse certificate from image
- `POST /certificate/store-blockchain` - Store certificate on blockchain
- `GET /certificate/blockchain/{hash}` - Get certificate from blockchain
- `POST /certificate/verify-comprehensive` - Full verification with AI + blockchain
- `POST /verify-faces` - Photo verification
- `POST /verify-signatures` - Signature verification

## 🛠️ Configuration

### Environment Variables (.env)

```env
# Hugging Face API Token (for AI models)
HF_API_TOKEN=your_token_here

# Blockchain Configuration
BLOCKCHAIN_RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# Model Paths (optional - will use mocks if not available)
SIGN_PARSER_MODEL_PATH=./models/sign_parser.pt
SIGN_VERIFIER_MODEL_PATH=./models/sign_verifier.keras
```

## 🧪 Testing

The system works in **mock mode** by default when AI models or blockchain are not available:

- **Mock AI Models**: Provides realistic responses for testing
- **Mock Blockchain**: Simulates blockchain operations
- **Real Integration**: Automatically switches to real services when available

## 📱 Usage

1. **Start both backend and frontend**
2. **Open http://localhost:5173**
3. **Navigate to Dashboard**
4. **Upload a certificate image**
5. **Choose operation**:
   - Parse Certificate (extract data)
   - Store on Blockchain (parse + store)
   - Verify by Hash (lookup existing)

## 🔒 Security Features

- CORS protection with specific origins
- Input validation and sanitization
- Error handling and logging
- Mock mode for safe testing

## 🏃‍♂️ Development

### Backend Development
```bash
cd Authenex/Backend
python start.py  # Auto-reload enabled
```

### Frontend Development
```bash
cd Authenex/Frontend
npm run dev  # Hot reload enabled
```

## 📦 Production Deployment

### Backend
```bash
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build
npm run preview
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details