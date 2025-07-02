## Unit Stats Extraction (Character Stats)

When extracting unit stats, from top to bottom the numbers represent:

- **Accuracy**: The ability to hit during combat. Add the accuracy value to the result of a d20 when making attacks to determine the total attack value. If the result equals or exceeds a target's defense, the attack HITS; otherwise, the attack GRAZES.
- **Power**: The unit's damage output. If the attack hits, the defender suffers full damage (the bigger number to the left of the slash); if the attack grazes, the defender suffers partial damage (the smaller number to the right of the slash).
- **Range**: The distance in inches the unit can make a ranged attack. If the stat is "0", the unit may only perform attacks on nearby enemies, but other game effects could increase this number.
- **Speed**: The distance in inches the unit can move in a single move action.
- **Defense**: The unit's defense threshold. The attack hits if the total attack value equals or exceeds its target's defense and grazes otherwise.
- **Max Health**: How much damage a unit can resist before being defeated. Use the damage tokens to track damage dealt to a unit, or its current health (referred simply as health). When the unit's health reaches 0, that unit is defeated.

## Card Anatomy Components

When analyzing card anatomy, extract the following components:

### Basic Card Elements
- **Card Name**: Identifies a specific card (appears at the top of the card)
- **Cost and Rank**: Most cards have a cost in echo to be played, represented by the number on the diamond. The color of the diamond indicates a card's rank:
  - Orange = Basic
  - Blue = Elite  
  - Yellow = Unique
  - Red = Legendary
- **Factions**: The card's faction affiliation is shown with one or more faction sigils
- **Card Type & Subtype**: Example types include unit, spell, and attachment. Cards can also be divided into subtypes, which highlight their particular characteristics and are used for some game effects.

### Unit-Specific Elements
- **Stats**: Specific to unit cards. This represents how capable a unit is at interactions on the battlefield. Stats are displayed as icons with numbers:
  - Accuracy (crosshair icon)
  - Power (explosion icon with slash notation for hit/graze damage)
  - Range (bow icon)
  - Speed (boot icon)
  - Defense (shield icon)
  - Max Health (heart icon)

### Card Effects
- **Text Box**: A detailed description of a card's effects. On a unit card, this box lists all of its abilities.

## Metadata Extraction Guidelines

When analyzing card anatomy, reference input/card-anatomy.png and input/character-stats.png
When asked to extract metadata from a card, write it to output/cards.md in a format ChatGPT will understand. Do not extract artist, copyright date, or language. Include:
- Card name
- Faction(s)
- Card rarity (basic, elite, unique, legendary)
- Card type and subtype(s)
- Cost (if applicable)
- Stats (for unit cards)
- Abilities and text box content
