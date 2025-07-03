<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>


## <h1 align="center" id="heading"> 👋 Welcome to the AI Engineer Challenge</h1>

## 🤖 Your First Vibe Coding LLM Application

> If you are a novice, and need a bit more help to get your dev environment off the ground, check out this [Setup Guide](docs/GIT_SETUP.md). This guide will walk you through the 'git' setup you need to get started.

> For additional context on LLM development environments and API key setup, you can also check out our [Interactive Dev Environment for LLM Development](https://github.com/AI-Maker-Space/Interactive-Dev-Environment-for-AI-Engineers).

In this repository, we'll walk you through the steps to create a LLM (Large Language Model) powered application with a vibe-coded frontend!

Are you ready? Let's get started!

<details>
  <summary>🖥️ Accessing "gpt-4.1-mini" (ChatGPT) like a developer</summary>

1. Head to [this notebook](https://colab.research.google.com/drive/1sT7rzY_Lb1_wS0ELI1JJfff0NUEcSD72?usp=sharing) and follow along with the instructions!

2. Complete the notebook and try out your own system/assistant messages!

That's it! Head to the next step and start building your application!

</details>


<details>
  <summary>🏗️ Forking & Cloning This Repository</summary>

Before you begin, make sure you have:

1. 👤 A GitHub account (you'll need to replace `YOUR_GITHUB_USERNAME` with your actual username)
2. 🔧 Git installed on your local machine
3. 💻 A code editor (like Cursor, VS Code, etc.)
4. ⌨️ Terminal access (Mac/Linux) or Command Prompt/PowerShell (Windows)
5. 🔑 A GitHub Personal Access Token (for authentication)

Got everything in place? Let's move on!

1. Fork [this](https://github.com/AI-Maker-Space/The-AI-Engineer-Challenge) repo!

     ![image](https://i.imgur.com/bhjySNh.png)

1. Clone your newly created repo.

     ``` bash
     # First, navigate to where you want the project folder to be created
     cd PATH_TO_DESIRED_PARENT_DIRECTORY

     # Then clone (this will create a new folder called The-AI-Engineer-Challenge)
     git clone git@github.com:<YOUR GITHUB USERNAME>/The-AI-Engineer-Challenge.git
     ```

     > Note: This command uses SSH. If you haven't set up SSH with GitHub, the command will fail. In that case, use HTTPS by replacing `git@github.com:` with `https://github.com/` - you'll then be prompted for your GitHub username and personal access token.

2. Verify your git setup:

     ```bash
     # Check that your remote is set up correctly
     git remote -v

     # Check the status of your repository
     git status

     # See which branch you're on
     git branch
     ```

     <!-- > Need more help with git? Check out our [Detailed Git Setup Guide](docs/GIT_SETUP.md) for a comprehensive walkthrough of git configuration and best practices. -->

3. Open the freshly cloned repository inside Cursor!

     ```bash
     cd The-AI-Engineering-Challenge
     cursor .
     ```

4. Check out the existing backend code found in `/api/app.py`

</details>

<details>
  <summary>🔥Setting Up for Vibe Coding Success </summary>

While it is a bit counter-intuitive to set things up before jumping into vibe-coding - it's important to remember that there exists a gradient betweeen AI-Assisted Development and Vibe-Coding. We're only reaching *slightly* into AI-Assisted Development for this challenge, but it's worth it!

1. Check out the rules in `.cursor/rules/` and add theme-ing information like colour schemes in `frontend-rule.mdc`! You can be as expressive as you'd like in these rules!
2. We're going to index some docs to make our application more likely to succeed. To do this - we're going to start with `CTRL+SHIFT+P` (or `CMD+SHIFT+P` on Mac) and we're going to type "custom doc" into the search bar. 

     ![image](https://i.imgur.com/ILx3hZu.png)
3. We're then going to copy and paste `https://nextjs.org/docs` into the prompt.

     ![image](https://i.imgur.com/psBjpQd.png)

4. We're then going to use the default configs to add these docs to our available and indexed documents.

     ![image](https://i.imgur.com/LULLeaF.png)

5. After that - you will do the same with Vercel's documentation. After which you should see:

     ![image](https://i.imgur.com/hjyXhhC.png) 

</details>

<details>
  <summary>😎 Vibe Coding a Front End for the FastAPI Backend</summary>

1. Use `Command-L` or `CTRL-L` to open the Cursor chat console. 

2. Set the chat settings to the following:

     ![image](https://i.imgur.com/LSgRSgF.png)

3. Ask Cursor to create a frontend for your application. Iterate as much as you like!

4. Run the frontend using the instructions Cursor provided. 

> NOTE: If you run into any errors, copy and paste them back into the Cursor chat window - and ask Cursor to fix them!

> NOTE: You have been provided with a backend in the `/api` folder - please ensure your Front End integrates with it!

</details>

<details>
  <summary>🚀 Deploying Your First LLM-powered Application with Vercel</summary>

1. Ensure you have signed into [Vercel](https://vercel.com/) with your GitHub account.

2. Ensure you have `npm` (this may have been installed in the previous vibe-coding step!) - if you need help with that, ask Cursor!

3. Run the command:

     ```bash
     npm install -g vercel
     ```

4. Run the command:

     ```bash
     vercel
     ```

5. Follow the in-terminal instructions. (Below is an example of what you will see!)

     ![image](https://i.imgur.com/D1iKGCq.png)

6. Once the build is completed - head to the provided link and try out your app!

> NOTE: Remember, if you run into any errors - ask Cursor to help you fix them!

</details>

### Vercel Link to Share

You'll want to make sure you share you *domains* hyperlink to ensure people can access your app!

![image](https://i.imgur.com/mpXIgIz.png)

> NOTE: Test this is the public link by trying to open your newly deployed site in an Incognito browser tab!

### 🎉 Congratulations! 

You just deployed your first LLM-powered application! 🚀🚀🚀 Get on linkedin and post your results and experience! Make sure to tag us at @AIMakerspace!

Here's a template to get your post started!

```
🚀🎉 Exciting News! 🎉🚀

🏗️ Today, I'm thrilled to announce that I've successfully built and shipped my first-ever LLM using the powerful combination of , and the OpenAI API! 🖥️

Check it out 👇
[LINK TO APP]

A big shoutout to the @AI Makerspace for all making this possible. Couldn't have done it without the incredible community there. 🤗🙏

Looking forward to building with the community! 🙌✨ Here's to many more creations ahead! 🥂🎉

Who else is diving into the world of AI? Let's connect! 🌐💡

#FirstLLMApp 
```

# PDF RAG Chat System

A modern web application that allows users to upload PDF documents and chat with them using AI-powered Retrieval-Augmented Generation (RAG). Built with FastAPI backend and React frontend, leveraging the `aimakerspace` library for document processing and vector search.

## Features

- 📄 **PDF Upload**: Upload PDF documents through a simple drag-and-drop interface
- 🔍 **Document Indexing**: Automatically extract and index PDF content using vector embeddings
- 💬 **RAG Chat**: Ask questions about your PDFs and get AI-powered responses based on document content
- 🚀 **Real-time Streaming**: Get responses streamed in real-time for better user experience
- 📚 **Multiple PDFs**: Upload and manage multiple PDF documents
- 🗑️ **Document Management**: Delete PDFs and their indexes when no longer needed

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI**: GPT models for chat completions and text embeddings
- **aimakerspace**: Custom library for document processing and vector search
- **PyPDF2**: PDF text extraction
- **NumPy**: Vector operations and similarity calculations

### Frontend
- **React**: Modern UI framework
- **Vite**: Fast build tool and development server
- **CSS3**: Modern styling with gradients and animations

## Architecture

### RAG System Flow
1. **PDF Upload**: User uploads a PDF file
2. **Text Extraction**: PDF content is extracted using PyPDF2
3. **Chunking**: Text is split into manageable chunks (1000 chars with 200 char overlap)
4. **Embedding**: Each chunk is converted to vector embeddings using OpenAI's text-embedding-3-small
5. **Vector Storage**: Embeddings are stored in an in-memory vector database
6. **Query Processing**: User questions are embedded and similar chunks are retrieved
7. **Context Generation**: Relevant chunks are combined to create context
8. **AI Response**: GPT model generates responses based on the context

### API Endpoints

- `POST /api/upload-pdf`: Upload and index a PDF
- `GET /api/pdfs`: List all uploaded PDFs
- `POST /api/chat`: Chat with a specific PDF using RAG
- `DELETE /api/pdfs/{pdf_id}`: Delete a PDF and its index
- `GET /api/health`: Health check endpoint

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup
```bash
cd api
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## Environment Variables

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Running the Application

### Development Mode

1. **Start the Backend**:
```bash
cd api
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

2. **Start the Frontend**:
```bash
cd frontend
npm run dev
```

3. **Access the Application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Production Mode

1. **Build the Frontend**:
```bash
cd frontend
npm run build
```

2. **Start the Backend**:
```bash
cd api
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Usage

1. **Enter API Key**: Provide your OpenAI API key in the designated field
2. **Upload PDF**: Click the file input to select and upload a PDF document
3. **Wait for Indexing**: The system will automatically extract text and create vector embeddings
4. **Select PDF**: Choose which PDF you want to chat with from the available documents
5. **Ask Questions**: Type your questions about the PDF content
6. **Get Responses**: Receive AI-generated answers based on the PDF content

## API Documentation

### Upload PDF
```bash
curl -X POST "http://localhost:8000/api/upload-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "api_key=your_openai_api_key"
```

### Chat with PDF
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "What is the main topic of this document?",
    "pdf_id": "your_pdf_id",
    "api_key": "your_openai_api_key"
  }'
```

## Configuration

### Chunking Parameters
- **Chunk Size**: 1000 characters (configurable in `process_pdf` function)
- **Chunk Overlap**: 200 characters (configurable in `process_pdf` function)

### Vector Search Parameters
- **Top-k Retrieval**: 3 most similar chunks (configurable in chat endpoint)
- **Embedding Model**: text-embedding-3-small (configurable in EmbeddingModel class)

### Chat Model
- **Default Model**: gpt-4o-mini (configurable in ChatRequest model)

## File Structure

```
The-AI-Engineer-Challenge/
├── api/
│   ├── app.py                 # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── uploads/              # PDF storage directory
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main React component
│   │   ├── App.css           # Styles
│   │   └── main.jsx          # React entry point
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
├── aimakerspace/             # Custom library
│   ├── text_utils.py         # PDF and text processing
│   ├── vectordatabase.py     # Vector search implementation
│   └── openai_utils/         # OpenAI utilities
└── README.md                 # This file
```

## Performance Considerations

- **Memory Usage**: Vector databases are stored in memory. For production, consider using persistent storage like PostgreSQL with pgvector
- **File Storage**: PDFs are stored locally. For production, consider cloud storage like AWS S3
- **Concurrent Users**: The current implementation uses in-memory storage. For multiple users, implement proper session management

## Security Considerations

- **API Key**: Never expose API keys in client-side code
- **File Validation**: Only PDF files are accepted
- **File Size**: Consider implementing file size limits
- **Rate Limiting**: Implement rate limiting for production use

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with the `aimakerspace` library for document processing
- Powered by OpenAI's GPT models and embeddings
- Modern UI design with React and CSS3
