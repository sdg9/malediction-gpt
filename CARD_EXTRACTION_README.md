# Card Metadata Extraction Script

This script automatically extracts metadata from Malediction card images using OpenRouter's LLM API and formats it as mar## File Structure

```text
├── src/
│   ├── extract_card_metadata.py  # Main extraction script
│   └── test_single_card.py       # Single card testing script
├── input/
│   └── cards/                    # Card images organized by faction
│       ├── faction_blue/         # Conclave of the Sphere cards
│       │   ├── card1.webp
│       │   ├── card2.webp
│       │   └── seeker/           # Seeker cards for this faction
│       │       ├── seeker.webp
│       │       └── legacy.webp
│       ├── faction_red/          # Primal Blood cards
│       ├── faction_green/        # Legion of the Fallen cards
│       ├── faction_yellow/       # Order of the Shattered Throne cards
│       ├── faction_blue_yellow/  # Dual faction cards
│       └── faction_none/         # Faction-neutral cards
├── output/
│   └── cards.md                  # Generated metadata with image links
├── .env.example                  # Environment template
├── .env                          # Your API key (create this)
└── requirements.txt              # Python dependencies
``` consumption by ChatGPT and other tools.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenRouter API key:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenRouter API key
   # Get an API key from https://openrouter.ai/
   ```

3. **Organize card images** in the faction-based folder structure:
   ```
   input/cards/
   ├── faction_blue/              # Conclave of the Sphere
   ├── faction_green/             # Legion of the Fallen  
   ├── faction_yellow/            # Order of the Shattered Throne
   ├── faction_red/               # Primal Blood
   ├── faction_none/              # Non-faction cards
   ├── faction_blue_yellow/       # Dual faction cards
   ├── faction_green_blue/        # Dual faction cards
   └── faction_yellow_red/        # Dual faction cards
       ├── card1.webp
       ├── card2.webp
       └── seeker/                # Seeker (leader) cards
           ├── seeker_card.webp
           └── legacy_card.webp
   ```

4. **Verify your setup:**
   ```bash
   # Check folder structure and dependencies
   python scripts/check_setup.py
   
   # Test with a single card first
   python src/test_single_card.py
   ```

## Usage

### Process All Cards
To extract metadata from all card images in `input/cards/` and append to `output/cards.md`:

```bash
python src/extract_card_metadata.py
```

### Test Single Card
To test the extraction with just one card:

```bash
python src/test_single_card.py
```

## How It Works

1. **Loads Instructions**: The script reads the card analysis instructions from `.github/copilot-instructions.md`

2. **Faction Detection**: Automatically determines card factions from the folder structure:
   - `faction_blue/` → Conclave of the Sphere
   - `faction_green/` → Legion of the Fallen
   - `faction_yellow/` → Order of the Shattered Throne
   - `faction_red/` → Primal Blood
   - `faction_blue_yellow/` → Dual faction cards
   - Cards in `seeker/` subfolders are identified as Seeker (leader) cards

3. **Image Processing**:
   - Recursively finds all image files in faction folders
   - Compresses images if they're larger than 4MB to stay within API limits
   - Converts images to base64 for API transmission

4. **LLM Analysis**:
   - Sends each image along with the instructions and faction context to OpenRouter
   - Uses Claude 3.5 Sonnet by default (configurable)
   - Extracts structured metadata according to the guidelines

5. **File Management**:
   - Extracts card name from the AI-generated metadata
   - Renames card files from generic names (e.g., `imgi_94_PE-111.webp`) to descriptive names (e.g., `runefold-ward.webp`)
   - Generates correct markdown image links with relative paths

6. **Output Generation**:
   - Formats results as markdown with card name headers
   - Includes markdown image links pointing to the renamed files
   - Appends to `output/cards.md` file
   - Includes rate limiting delays between API calls

## Features

- **Faction Detection**: Automatically determines card factions from folder structure
- **Rate Limiting**: Configurable delays between API calls to respect rate limits
- **Image Compression**: Automatically compresses large images to stay within API limits
- **File Renaming**: Renames card files from generic names to descriptive card names
- **Smart Linking**: Generates correct relative path links for renamed files
- **Error Handling**: Continues processing even if individual cards fail
- **Progress Tracking**: Shows progress and success/failure counts
- **Resume Support**: Can append to existing output files
- **Seeker Detection**: Identifies and labels faction leader cards

## Configuration

The script uses several configurable parameters:

- **Model**: Default is `anthropic/claude-3.5-sonnet` but can be changed in the code
- **Delay**: Default 1 second between API calls, adjustable for different rate limits
- **Image Size**: Compresses images larger than 4MB

## Output Format

The script generates markdown in the format specified in the instructions:

```markdown
# Card Name

- **Faction(s)**: Faction Name
- **Card Rarity**: Basic/Elite/Unique/Legendary
- **Card Type**: Unit/Spell/Attachment
- **Subtype(s)**: Relevant subtypes
- **Cost**: Echo cost (if applicable)
- **Stats** (for unit cards):
  - **Accuracy**: X
  - **Power**: X/X
  - **Range**: X
  - **Speed**: X
  - **Defense**: X
  - **Max Health**: X
- **Abilities**: 
  - Description of abilities and effects
```

## Troubleshooting

### API Key Issues
- Ensure your `.env` file is in the project root
- Verify your OpenRouter API key is correct
- Check that you have credits/permissions on OpenRouter

### Image Processing Issues
- Ensure PIL (Pillow) is installed: `pip install Pillow`
- Verify card images are in supported formats (webp, jpg, png)
- Check that input/cards directory exists and contains images

### Rate Limiting
- Increase the delay between requests if you hit rate limits
- Some OpenRouter models have different rate limits
- Consider using a different model if needed

## File Structure

```
├── src/
│   ├── extract_card_metadata.py  # Main extraction script
│   └── test_single_card.py       # Single card testing script
├── input/
│   └── cards/                    # Card images (webp, jpg, png)
├── output/
│   └── cards.md                  # Generated metadata
├── .env.example                  # Environment template
├── .env                          # Your API key (create this)
└── requirements.txt              # Python dependencies
```
