# Malediction Rules GPT and supporting scripts

This project converts [Malediction](https://malediction.gg/) rules and FAQ PDF files to text format with page markers to be used in the custom GPT [Malediction Rules GPT](https://chatgpt.com/g/g-6858afa830ac8191a288e426bcb90976-malediction-rules-gpt)

If you only want to ask questions about the Malediction rules, you can use the [Malediction Rules GPT](https://chatgpt.com/g/g-6858afa830ac8191a288e426bcb90976-malediction-rules-gpt) directly without needing to run this code.

This repo provides a Python script to extract text from the Malediction RPG PDF files and save them in a structured format with page markers to aid in creation of the custom GPT.

## Setup Instructions

### 1. Create a Python Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 2. Install Required Dependencies

```bash
# Install dependencies from requirements.txt
pip install -r requirements.txt
```

### 3. Prepare Your Files

Place your PDF files in the `input/` folder. The script will automatically detect and process all PDF files in this directory.

### 4. Run the PDF to Text Converter

```bash
python3 src/pdfToText.py
```

This will:

- Automatically detect all PDF files in the `input/` folder
- Extract text from all pages with page markers
- Save output files to the `output/` folder with the same name but `.txt` extension
- Example: `Malediction_BasicRules_Ver1-compact.pdf` → `Malediction_BasicRules_Ver1-compact.txt`

## Project Structure

```text
malediction-gpt/
├── input/                              # Place your PDF files here
│   ├── Malediction_BasicRules_Ver1-compact.pdf
│   └── Malediction_FAQ_MAY25_rev_2.pdf
├── output/                             # Generated text files
│   ├── Malediction_BasicRules_Ver1-compact.txt
│   └── Malediction_FAQ_MAY25_rev_2.txt
├── src/                                # Source code
│   └── pdfToText.py
├── venv/                               # Virtual environment (created after setup)
├── requirements.txt                    # Python dependencies
├── CONTRIBUTING.md                     # Contribution guidelines
├── LICENSE                             # Public domain license
├── README.md
└── .gitignore
```

## Available Files

- `src/pdfToText.py` - Python script to convert PDF to text
- `requirements.txt` - Python dependencies

## Notes

- Make sure to activate the virtual environment before running the script
- The script automatically detects and processes **all PDF files** in the `input/` folder
- Output files preserve the original filename with `.txt` extension
- Output files include page numbers in `[Page X]` format
- The `output/` folder will be created automatically if it doesn't exist
- The script handles errors gracefully and reports processing results

## Deactivating the Virtual Environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```

## Custom GPT

As of this writing I'm not aware of a programmatic way to update ChatGPT's custom GPTs, otherwise I would love a github actions workflow to automatically update the custom GPT with each commit.

Short of that I manually upload both the input and output artifacts to the custom GPT at [Malediction Rules GPT](https://chatgpt.com/g/g-6858afa830ac8191a288e426bcb90976-malediction-rules-gpt).

### Custom GPT Instructions

FYI my current GPT instructions for the Malediction Rules GPT are:

```text
## 📖 Source Referencing

- Ingest the `.txt` version first—use its page markers for quotations.
- Use the PDF/FAQ as secondary reference when users mention diagrams or casting doubt on your text quotes.
- The uploaded documents have **page number annotations** embedded in the text.
- When providing an answer, **include the page number** where the information is found, formatted like:
  > “See page 12 of the rulebook.”
- If the exact page is unclear or missing, say:
  > “I’m not sure which page this appears on—please check the official documents.”

## ✅ Behavior Guidelines
1. **Be precise** and **concise**, no fluff.  
2. **Use bullet points or numbered lists** for clarity when detailing rules or steps.  
3. **Ask follow‑up questions** if a user’s query is ambiguous.  
4. **Don’t hallucinate**—only state what is in the official sources.


## ✅ Workflow

1. Read the user question.  
2. Search the ingested text (with page markers) for relevant information.  
3. Quote verbatim or paraphrase as needed.  
4. End your answer with:  
   > “(Found on page X of the Malediction Rulebook/FAQ.)”
5. If you can’t find it, respond:
   > “I didn’t find that in the documents—please check the official PDF or FAQ.”

## 🛠 Example  
> **User:** “What's the deploy phase limit?”  
> **GPT:**  
> “As long as the player has sufficient echo, there is no limit to the number of units they can deploy in a single round. (Pg 13 of the Ver1 rulebook)”
```

## License

This project is released into the **public domain** under The Unlicense - see the [LICENSE](LICENSE) file for details.

This means:

- **No copyright** - You can do absolutely anything with this code
- **No attribution required** - You don't need to credit the original author
- **No restrictions** - Use commercially, modify, distribute, sell, etc.
- **Public domain** - The code belongs to everyone and no one
