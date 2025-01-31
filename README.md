# Agent-Foundry

Welcome to **Agent-Foundry**, a repository for developing and experimenting with LLM-based agents using [LangGraph](https://github.com/langchain-ai/langgraph). This project focuses on modular agent architectures and multi-agent collaboration.

---

## 🛠 Features

1. **Simple LLM Agents**: Core logic understanding.
2. **Multi-Agent Systems**: Complex workflows and interactions.
3. **Custom Tool Integrations**: Extend capabilities with APIs, web search, and utilities.

---

## 📊 Graph Implementations

- **BasicGraph**: `./01/graph.py`
- **Graph with customReducer**: `./02/graph.py`
- **Calculator_agent**: `./03/graph.py`
- **Summary_keeping_agent**: `./04/graph.py`
- **More planned implementations**

---

## 🔧 Future Agent Ideas

- **Conversational Assistant**: Context-aware chat with personality customization.
- **Math Solver**: Step-by-step problem solving with calculator integration.
- **File Management Agent**: Organizes, renames, and moves files.
- **Weather Agent**: Retrieves and summarizes weather forecasts.
- **Task Scheduler**: Manages calendar events and reminders.
- **News Summarizer**: Fetches, categorizes, and summarizes articles.
- **Document Q&A**: Parses and answers queries based on documents.
- **Translation Agent**: Multi-language support and text translation.
- **Code Helper**: Syntax checking, debugging, and explanations.
- **Research Assistant**: Web search, information extraction, and source verification.
- **Multi-Agent Collaboration**: Task distribution, agent interaction, and conflict resolution.
- **AI Image Analysis**: Object detection and image description generation.
- **Data Analysis Agent**: Statistical processing and visualization generation.
- **Smart Automation**: IoT integration and rule-based automation.
- **Content Creation**: SEO-optimized article structuring and topic research.

### Development Roadmap:
1. **Phase 1**: Build foundational agents with LangChain.
2. **Phase 2**: Integrate orchestration, API enhancements, and logging.
3. **Phase 3**: Explore frameworks like AutoGen, CrewAI for scalable solutions.

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sayemahamed/Agent-Foundry.git
   cd Agent-Foundry
   ```

2. **Set up a Python virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install LangGraph in development mode (optional for contributions):**
   ```bash
   pip install -e .[dev]
   ```
   
4. **Run langgraph (in dev mode)**
   ```bash
   langgraph dev
   ```
---

## 🏆 Acknowledgments

This project utilizes several key packages, including but not limited to:

- **LangGraph**: Graph-based agent workflows.
- **LangChain**: Modular LLM integrations.
- **Ollama**: Local LLM serving.
- **Groq**: Optimized inference for LLMs.
- **FAISS**: Vector search and retrieval.
- **SQLAlchemy**: Database interactions.
- **Requests & HTTPX**: Web interactions.
- **BeautifulSoup4**: Web scraping.
- **Tiktoken**: Tokenization for LLMs.

Special thanks to open-source contributors making AI development accessible.

---

## 🤝 Contributions

Contributions are welcome! Submit issues, fork the repo, or create pull requests.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For inquiries, reach out via:
- **Email**: [sayemahamed183@gmail.com](mailto:sayemahamed183@gmail.com)
- **GitHub**: [Agent-Foundry](https://github.com/Sayemahamed/Agent-Foundry)

