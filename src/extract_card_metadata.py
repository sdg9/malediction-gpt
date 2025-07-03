#!/usr/bin/env python3
"""
Script to extract metadata from Malediction card images using OpenRouter LLM.
Iterates through all card images and generates markdown metadata for each card.
"""

import os
import sys
import base64
import json
import time
import glob
from pathlib import Path
from typing import Optional, Dict, Any
import requests
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CardMetadataExtractor:
    # def __init__(self, openrouter_api_key: str, model: str = "openai/gpt-4o"):
    def __init__(self, openrouter_api_key: str, model: str = "openai/gpt-4o-mini"):
        """
        Initialize the card metadata extractor.

        Args:
            openrouter_api_key: OpenRouter API key
            model: The model to use for analysis (default: Claude 3.5 Sonnet)
        """
        self.api_key = openrouter_api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/sdg9/malediction-gpt",
            "X-Title": "Malediction Card Metadata Extractor"
        }

        # Load instructions from copilot-instructions.md
        self.instructions = self._load_instructions()

    def _load_instructions(self) -> str:
        """Load the card analysis instructions from copilot-instructions.md"""
        instructions_path = Path(__file__).parent.parent / \
            ".github" / "copilot-instructions.md"
        try:
            with open(instructions_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(
                f"Warning: Instructions file not found at {instructions_path}")
            return ""

    def _encode_image_to_base64(self, image_path: str) -> str:
        """Convert image file to base64 string."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image {image_path}: {e}")
            return ""

    def _compress_image_if_needed(self, image_path: str, max_size_mb: float = 4.0) -> Optional[str]:
        """
        Compress image if it's too large for the API.

        Args:
            image_path: Path to the image file
            max_size_mb: Maximum size in MB

        Returns:
            Path to the processed image (original or compressed)
        """
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        if file_size_mb <= max_size_mb:
            return image_path

        # Create a compressed version
        try:
            img = Image.open(image_path)

            # Calculate new dimensions to reduce file size
            reduction_factor = (max_size_mb / file_size_mb) ** 0.5
            new_width = int(img.width * reduction_factor)
            new_height = int(img.height * reduction_factor)

            # Resize image
            img_resized = img.resize(
                (new_width, new_height), Image.Resampling.LANCZOS)

            # Save compressed image
            compressed_path = image_path.replace('.webp', '_compressed.webp')
            img_resized.save(compressed_path, 'WEBP', quality=85)

            print(
                f"Compressed {image_path} from {file_size_mb:.2f}MB to {os.path.getsize(compressed_path)/(1024*1024):.2f}MB")
            return compressed_path

        except Exception as e:
            print(f"Error compressing image {image_path}: {e}")
            return image_path

    def _extract_faction_from_path(self, image_path: str) -> Dict[str, Any]:
        """
        Extract faction information from the file path.
        
        Args:
            image_path: Path to the card image
            
        Returns:
            Dictionary with faction info and card type
        """
        path_parts = Path(image_path).parts
        
        # Find the faction folder in the path
        faction_info = {
            'factions': [],
            'is_seeker': False,
            'card_type': 'Regular'
        }
        
        for part in path_parts:
            if part.startswith('faction_'):
                # Extract faction colors from folder name
                faction_part = part.replace('faction_', '')
                
                if faction_part == 'none':
                    faction_info['factions'] = ['None']
                else:
                    # Split by underscore for dual factions
                    colors = faction_part.split('_')
                    
                    # Map colors to faction names
                    color_to_faction = {
                        'blue': 'Conclave of the Sphere',
                        'green': 'Legion of the Fallen', 
                        'yellow': 'Order of the Shattered Throne',
                        'red': 'Primal Blood'
                    }
                    
                    faction_info['factions'] = [color_to_faction.get(color, color) for color in colors]
                
                break
        
        # Check if it's a seeker card
        if 'seeker' in path_parts:
            faction_info['is_seeker'] = True
            faction_info['card_type'] = 'Seeker'
        
        return faction_info

    def _clean_markdown_response(self, content: str) -> str:
        """
        Clean up the LLM response by removing unwanted markdown code blocks.
        
        Args:
            content: Raw response from the LLM
            
        Returns:
            Cleaned markdown content
        """
        if not content:
            return content
            
        # Remove markdown code block wrapping
        content = content.strip()
        
        # Remove leading ```markdown or ``` 
        if content.startswith('```markdown'):
            content = content[11:].strip()
        elif content.startswith('```'):
            content = content[3:].strip()
            
        # Remove trailing ```
        if content.endswith('```'):
            content = content[:-3].strip()
            
        return content

    def extract_metadata(self, image_path: str) -> Optional[str]:
        """
        Extract metadata from a single card image using OpenRouter.

        Args:
            image_path: Path to the card image

        Returns:
            Extracted metadata as markdown string, or None if failed
        """
        # Extract faction information from path
        faction_info = self._extract_faction_from_path(image_path)
        
        # Compress image if needed
        processed_image_path = self._compress_image_if_needed(image_path)
        if not processed_image_path:
            return None

        # Encode image to base64
        image_base64 = self._encode_image_to_base64(processed_image_path)
        if not image_base64:
            return None

        # Clean up compressed file if it was created
        if processed_image_path != image_path:
            try:
                os.remove(processed_image_path)
            except:
                pass

        # Build faction context for the prompt
        faction_context = ""
        if faction_info['factions']:
            if len(faction_info['factions']) == 1:
                faction_context = f"\n\nBased on the file path, this card belongs to the {faction_info['factions'][0]} faction."
            else:
                faction_names = " and ".join(faction_info['factions'])
                faction_context = f"\n\nBased on the file path, this card has dual faction affiliation: {faction_names}."
        
        if faction_info['is_seeker']:
            faction_context += " This is a Seeker card (faction leader)."

        # Prepare the prompt
        prompt = f"""
{self.instructions}

Please analyze this Malediction card image and extract the metadata according to the guidelines above.{faction_context}

Return the metadata in the exact format specified in the instructions:
- Use the card name as the header (# Card Name)
- Include all required fields as bullet points
- For unit cards, include all stats with their values
- Include all abilities and text from the card
- Do not include artist, copyright, language, or flavor text
- Do not include an image link in the output (this will be added automatically)

IMPORTANT: Return only the raw markdown content without any code block formatting (no ```markdown or ``` tags). The output should be direct markdown content that can be appended to a .md file.
"""

        # Prepare the API request
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/webp;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1000,
            "temperature": 0.1
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    raw_content = result['choices'][0]['message']['content'].strip()
                    cleaned_content = self._clean_markdown_response(raw_content)
                    return cleaned_content
                else:
                    print(f"No choices in response for {image_path}")
                    return None
            else:
                print(
                    f"API request failed for {image_path}: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error making API request for {image_path}: {e}")
            return None

    def process_all_cards(self, input_dir: str, output_file: str, delay_seconds: float = 1.0):
        """
        Process all card images in the input directory and its faction subdirectories.

        Args:
            input_dir: Directory containing faction folders with card images
            output_file: Path to the output markdown file
            delay_seconds: Delay between API calls to respect rate limits
        """
        # Find all card image files recursively in faction folders
        card_files = []
        input_path = Path(input_dir)
        
        # Supported image extensions
        image_extensions = ['*.webp', '*.jpg', '*.jpeg', '*.png']
        
        # Search recursively through all subdirectories
        for extension in image_extensions:
            # Use rglob for recursive search from the input path
            found_files = input_path.rglob(extension)
            card_files.extend([str(f) for f in found_files])
        
        # Filter out .DS_Store and other non-card files
        card_files = [
            f for f in card_files 
            if not os.path.basename(f).startswith('.') 
            and 'faction_' in f  # Only include files in faction folders
        ]
        card_files.sort()  # Process in consistent order

        print(f"Found {len(card_files)} card images to process across faction folders")
        
        # Group by faction for reporting
        faction_counts = {}
        for card_file in card_files:
            faction_info = self._extract_faction_from_path(card_file)
            if faction_info['factions']:
                faction_key = " + ".join(faction_info['factions'])
                if faction_info['is_seeker']:
                    faction_key += " (Seeker)"
                faction_counts[faction_key] = faction_counts.get(faction_key, 0) + 1
        
        print("Cards by faction:")
        for faction, count in sorted(faction_counts.items()):
            print(f"  {faction}: {count} cards")

        # Check if output file exists and ask for confirmation
        if os.path.exists(output_file):
            response = input(
                f"Output file {output_file} exists. Append to it? (y/n): ")
            if response.lower() != 'y':
                print("Exiting...")
                return

        # Process each card
        successful = 0
        failed = 0
        project_root = str(Path(input_dir).parent)  # Get project root for relative paths

        with open(output_file, 'a', encoding='utf-8') as f:
            for i, card_file in enumerate(card_files, 1):
                # Get faction info for display
                faction_info = self._extract_faction_from_path(card_file)
                faction_display = " + ".join(faction_info['factions']) if faction_info['factions'] else "Unknown"
                if faction_info['is_seeker']:
                    faction_display += " (Seeker)"
                
                print(f"Processing {i}/{len(card_files)}: {os.path.basename(card_file)} [{faction_display}]")

                metadata = self.extract_metadata(card_file)

                if metadata:
                    # Extract card name from metadata
                    card_name = self._extract_card_name_from_metadata(metadata)
                    
                    if card_name:
                        # Rename the file to use the card name
                        renamed_file = self._rename_card_file(card_file, card_name)
                        
                        # Generate the markdown image link
                        image_link = self._generate_markdown_image_link(card_name, renamed_file, project_root)
                        
                        # Add the image link to the metadata
                        metadata_with_link = f"{metadata}\n\n{image_link}"
                        
                        f.write(f"\n{metadata_with_link}\n\n")
                    else:
                        # Fallback: use metadata without renaming if card name extraction fails
                        print(f"    Warning: Could not extract card name, keeping original filename")
                        f.write(f"\n{metadata}\n\n")
                    
                    f.flush()  # Ensure data is written immediately
                    successful += 1
                    print(f"  ✓ Successfully extracted metadata")
                else:
                    failed += 1
                    print(f"  ✗ Failed to extract metadata")

                # Add delay between requests to respect rate limits
                if i < len(card_files):  # Don't delay after the last card
                    time.sleep(delay_seconds)

        print(f"\nProcessing complete!")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Results written to: {output_file}")

    def _sanitize_filename(self, name: str) -> str:
        """
        Convert card name to a safe filename.
        
        Args:
            name: Card name from metadata
            
        Returns:
            Sanitized filename safe for filesystem
        """
        # Remove or replace unsafe characters
        name = name.strip()
        # Replace spaces with hyphens
        name = name.replace(' ', '-')
        # Remove unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            name = name.replace(char, '')
        # Replace multiple hyphens with single hyphen
        while '--' in name:
            name = name.replace('--', '-')
        # Remove leading/trailing hyphens
        name = name.strip('-')
        # Convert to lowercase
        name = name.lower()
        return name
    
    def _extract_card_name_from_metadata(self, metadata: str) -> Optional[str]:
        """
        Extract the card name from the generated metadata.
        
        Args:
            metadata: The generated markdown metadata
            
        Returns:
            Card name if found, None otherwise
        """
        lines = metadata.strip().split('\n')
        for line in lines:
            if line.startswith('# '):
                # Extract card name from header
                card_name = line[2:].strip()
                return card_name
        return None
    
    def _rename_card_file(self, old_path: str, card_name: str) -> str:
        """
        Rename card file to use the card name.
        
        Args:
            old_path: Current path to the card file
            card_name: Name of the card
            
        Returns:
            New path to the renamed file
        """
        old_file = Path(old_path)
        safe_name = self._sanitize_filename(card_name)
        
        # Keep the original extension
        extension = old_file.suffix
        
        # Create new filename
        new_filename = f"{safe_name}{extension}"
        new_path = old_file.parent / new_filename
        
        # Rename the file
        try:
            old_file.rename(new_path)
            print(f"    Renamed: {old_file.name} → {new_filename}")
            return str(new_path)
        except Exception as e:
            print(f"    Warning: Could not rename file {old_path}: {e}")
            return old_path
    
    def _generate_markdown_image_link(self, card_name: str, image_path: str, project_root: str) -> str:
        """
        Generate the markdown image link for the card.
        
        Args:
            card_name: Name of the card
            image_path: Full path to the image file
            project_root: Root directory of the project
            
        Returns:
            Markdown image link
        """
        # Convert to relative path from project root
        try:
            relative_path = os.path.relpath(image_path, project_root)
            # Ensure forward slashes for consistency
            relative_path = relative_path.replace('\\', '/')
            return f"![{card_name}]({relative_path})"
        except Exception as e:
            print(f"    Warning: Could not generate relative path for {image_path}: {e}")
            return f"![{card_name}]({image_path})"

def main():
    """Main function to run the card metadata extractor."""
    # Check for required environment variable
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your-api-key-here'")
        return 1

    # Set up paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    input_dir = project_root / "input" / "cards"
    output_file = project_root / "output" / "cards.md"

    # Verify input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return 1

    # Create output directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Initialize extractor
    extractor = CardMetadataExtractor(api_key)

    # Process all cards
    try:
        extractor.process_all_cards(str(input_dir), str(output_file))
        return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
