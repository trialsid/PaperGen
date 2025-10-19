# PaperGen

A comprehensive Python-based tool for generating professional educational question papers in PDF format. Supports multiple question types including MCQ, Match the Following (MTF), Statements evaluation, and more with advanced formatting capabilities. Includes AI-powered question generation using Google's Gemini.

## Features

- **Enhanced MCQ Paper Generation**: Create sophisticated multiple choice question papers with various question types
- **AI Question Generation**: Generate questions automatically using Google's Gemini AI (`json_generator.py`)
- **Multiple Question Formats**:
  - Basic Multiple Choice Questions
  - Match the Following (MTF) with optional headers
  - Statement evaluation (single and multiple statements)
  - List-based questions
  - Paragraph-based reading comprehension
  - Sequencing questions
  - Combinations of multiple formats in a single question
- **Professional PDF Output**: High-quality PDF generation with proper formatting and spacing
- **Multiple Paper Sets**: Generate multiple shuffled sets (A, B, C, etc.) from the same question bank
- **A3 Booklet Generation**: Automatically create A3 booklet-formatted PDFs with proper page ordering for printing
- **Flexible Font Sizing**: Four size configurations (x-small, small, medium, large) for different requirements
- **Comprehensive Answer Keys**:
  - Separate answer key PDFs with explanations
  - CSV format for quick reference across all sets
  - Detailed JSON with complete metadata
- **Advanced Formatting**: Two-column layout with smart question placement and height estimation
- **Unicode Font Support**: Full Unicode support with Arial Unicode and Noto fonts

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For AI question generation, create a `.env` file with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Basic Paper Generation

Generate a single paper set from a JSON file:

```bash
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json
```

This generates 2 sets (A and B) by default with:
- Question papers in `Generated_Papers/MCQ/Enhanced/Questions/`
- Answer keys in `Generated_Papers/MCQ/Enhanced/Answers/`
- A3 booklets in `Generated_Papers/MCQ/Enhanced/Booklets/`
- CSV answer key in `Generated_Papers/MCQ/Enhanced/`

### Advanced Options

```bash
# Generate 4 sets with custom titles
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json \
  --num-sets 4 \
  --title "Springfield High School" \
  --subtitle "123 Main Street, Springfield" \
  --exam-title "Mid-Term Examination 2025"

# Generate compact version without student info
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json \
  --size x-small \
  --no-student-info

# Generate without shuffling (same order in all sets)
python enhanced_mcq_paper_builder.py --input-file questions_data/example.json \
  --no-shuffle
```

### AI Question Generation

Generate questions using AI:

```bash
python json_generator.py
```

You'll be prompted to enter a topic, and the script will generate 20 questions in the correct JSON format.

### Command Line Options

| Option | Description |
|--------|-------------|
| `--input-file` | Path to questions JSON file (default: `questions_data/mcq_questions.json`) |
| `--num-sets` | Number of paper sets to generate (default: 2) |
| `--title` | School/Institute name (max 60 characters) |
| `--subtitle` | Address or additional info (max 50 characters) |
| `--exam-title` | Exam name (max 50 characters) |
| `--size` | Font and spacing size: `x-small`, `small`, `medium`, `large` (default: `medium`) |
| `--no-student-info` | Remove student information section from first page |
| `--no-shuffle` | Disable question and option shuffling (all sets will be identical) |
| `--layout` | Layout type: `one-column`, `two-column` (default: `two-column`) *Note: one-column not fully implemented* |

## File Structure

```
PaperGen/
├── enhanced_mcq_paper_builder.py    # Main script for generating papers
├── json_generator.py                # AI-powered question generator
├── paper_generators/                # Core PDF generation modules
│   ├── enhanced_mcq_generator.py   # Enhanced MCQ generator with all question types
│   ├── mcq_generator.py            # Base MCQ generator class
│   ├── base_generator.py           # Base PDF generator
│   ├── mixed_generator.py          # Mixed question type generator
│   └── styles.py                   # Font sizing and spacing configurations
├── questions_data/                  # Question bank files
│   ├── example.json                # Comprehensive example with all question types
│   ├── example2.json               # Additional examples
│   └── prompt.txt                  # AI prompt documentation
├── Generated_Papers/                # Output directory (auto-created)
│   └── MCQ/Enhanced/
│       ├── Questions/              # Question paper PDFs
│       ├── Answers/                # Answer key PDFs
│       ├── Booklets/               # A3 booklet PDFs
│       ├── enhanced_mcq_answer_keys.csv
│       └── enhanced_mcq_answer_keys_detailed.json
├── fonts/                          # Unicode font files
├── scripts/                        # Utility scripts
└── tests/                          # Test files
```

## Question Format

Questions are organized in sections within JSON files. The system supports multiple question types with flexible formatting using a universal array-based system.

### Basic Structure

```json
{
  "metadata": {
    "title": "Springfield High School",
    "subtitle": "123 Main Street, Springfield",
    "exam_title": "Mid-Term Examination"
  },
  "sections": [
    {
      "name": "Section Name",
      "description": "Section description or instructions",
      "questions": [...]
    }
  ]
}
```

**Note:** The `metadata` field is optional. The system uses a fallback chain to determine paper titles.

### Metadata Fallback Chain

Paper titles are determined by this **priority order**:

1. **CLI Arguments** (highest priority) - `--title`, `--subtitle`, `--exam-title`
2. **JSON Metadata** - Optional `metadata` object in input JSON file
3. **Sensible Defaults** (lowest priority) - Auto-generated from input filename

**Examples:**

```bash
# Priority 1: Using CLI arguments (overrides everything)
python enhanced_mcq_paper_builder.py --input-file test.json \
  --title "Springfield High School" \
  --subtitle "Main Campus" \
  --exam-title "Final Exam"

# Priority 2: Using JSON metadata (if no CLI args provided)
# Add this to your JSON file:
# {
#   "metadata": {
#     "title": "Springfield High School",
#     "subtitle": "Main Campus",
#     "exam_title": "Final Exam"
#   },
#   "sections": [...]
# }

# Priority 3: Defaults (if neither CLI nor metadata)
# Generates: "MCQ Paper - test" as title
```

### Question Types and Examples

#### 1. Basic MCQ Question

Simple multiple choice with text and options:

```json
{
  "question_text": ["What is the chemical symbol for water?"],
  "choices": ["H2O", "CO2", "NaCl", "O2"],
  "answer": "H2O",
  "reasoning": "Water is composed of two hydrogen atoms and one oxygen atom."
}
```

#### 2. Multi-line Question

Each string in `question_text` array creates a new line:

```json
{
  "question_text": [
    "A light ray travels from air into glass.",
    "What phenomenon occurs at the boundary?"
  ],
  "choices": [
    "Reflection only",
    "Refraction only",
    "Both reflection and refraction",
    "Neither"
  ],
  "answer": "Both reflection and refraction",
  "reasoning": "When light travels between media, both reflection and refraction occur."
}
```

#### 3. Statement Evaluation (Single Statement)

Uses the `STATEMENT` placeholder:

```json
{
  "question_text": [
    "Consider the following statement about gravity:",
    "STATEMENT",
    "Is this statement scientifically accurate?"
  ],
  "statements": [
    {
      "label": "Statement",
      "text": "Objects with greater mass exert stronger gravitational force."
    }
  ],
  "choices": ["True", "False", "True only on Earth", "True only in space"],
  "answer": "True",
  "reasoning": "Newton's law states gravitational force is proportional to mass."
}
```

#### 4. Statement Evaluation (Multiple Statements)

Uses the `STATEMENTS` placeholder for multiple statements:

```json
{
  "question_text": [
    "Evaluate the following statements:",
    "STATEMENTS",
    "Which statement(s) are correct?"
  ],
  "statements": [
    {
      "label": "Statement-1",
      "text": "The Earth revolves around the Sun."
    },
    {
      "label": "Statement-2",
      "text": "The Moon is a natural satellite of Earth."
    }
  ],
  "choices": ["1 only", "2 only", "Both 1 and 2", "Neither 1 nor 2"],
  "answer": "Both 1 and 2",
  "reasoning": "Both statements are scientifically accurate."
}
```

#### 5. Match the Following (MTF)

Uses the `MTF_DATA` placeholder with optional headers:

```json
{
  "question_text": ["Match the countries with their capitals:", "MTF_DATA"],
  "mtf_data": {
    "left_header": "Countries",
    "right_header": "Capitals",
    "left_column": ["A. France", "B. Germany", "C. Italy"],
    "right_column": ["Berlin", "Rome", "Paris"]
  },
  "choices": [
    "A-3, B-1, C-2",
    "A-1, B-2, C-3",
    "A-2, B-3, C-1",
    "A-3, B-2, C-1"
  ],
  "answer": "A-3, B-1, C-2",
  "reasoning": "France-Paris, Germany-Berlin, Italy-Rome"
}
```

#### 6. Paragraph-Based Question

Uses the `PARAGRAPH` placeholder:

```json
{
  "question_text": [
    "Read the following passage:",
    "PARAGRAPH",
    "What is required for chemical reactions to occur?"
  ],
  "paragraph": "Chemical reactions require activation energy to proceed. This energy barrier must be overcome for reactants to transform into products.",
  "choices": [
    "Low temperature",
    "Activation energy",
    "High pressure",
    "Presence of water"
  ],
  "answer": "Activation energy",
  "reasoning": "The passage explicitly states that activation energy is required."
}
```

#### 7. List-Based Question

Uses the `LIST` placeholder:

```json
{
  "question_text": [
    "Consider the following properties of metals:",
    "LIST",
    "Which property is NOT typically associated with metals?"
  ],
  "list_items": [
    "1. Good conductors of electricity",
    "2. Malleable and ductile",
    "3. Low melting points",
    "4. Lustrous appearance"
  ],
  "choices": [
    "Property 1",
    "Property 2",
    "Property 3",
    "Property 4"
  ],
  "answer": "Property 3",
  "reasoning": "Most metals have high melting points, not low ones."
}
```

#### 8. Combination Question

Combine multiple formats in one question:

```json
{
  "question_text": [
    "Read the passage carefully:",
    "PARAGRAPH",
    "Now evaluate the following statements:",
    "STATEMENTS",
    "Based on the passage, which statement(s) are correct?"
  ],
  "paragraph": "Photosynthesis is the process by which plants convert light energy into chemical energy.",
  "statements": [
    {
      "label": "Statement-1",
      "text": "Photosynthesis requires sunlight."
    },
    {
      "label": "Statement-2",
      "text": "Photosynthesis produces oxygen as a byproduct."
    }
  ],
  "choices": ["1 only", "2 only", "Both 1 and 2", "Neither"],
  "answer": "Both 1 and 2",
  "reasoning": "Both statements are consistent with the passage and scientific facts."
}
```

### Universal Question Text Array System

The `question_text` array is processed sequentially, and special keywords trigger different rendering:

- **Regular text**: Rendered as italic question text
- **`STATEMENT`** or **`STATEMENTS`**: Renders formatted statement(s) from `statements` array
- **`MTF_DATA`**: Renders match-the-following table from `mtf_data` object
- **`PARAGRAPH`**: Renders indented paragraph from `paragraph` field
- **`LIST`**: Renders formatted list from `list_items` array

This allows you to combine multiple formats by using placeholders in the correct sequence.

## Font Size Configurations

Choose from four predefined size configurations:

| Size | Description | Use Case |
|------|-------------|----------|
| **x-small** | Ultra-compact formatting | Maximum content density, long exams |
| **small** | Compact formatting | Space efficiency with readability |
| **medium** | Balanced formatting (default) | Standard exams |
| **large** | Spacious formatting | Better readability, younger students |

Each configuration adjusts font sizes, spacing, and layout proportionally for consistent appearance.

## Output Files

When you run the generator, it creates:

### 1. Question Papers
- **Location**: `Generated_Papers/MCQ/Enhanced/Questions/`
- **Format**: `enhanced_mcq_set_A.pdf`, `enhanced_mcq_set_B.pdf`, etc.
- **Content**: Two-column layout with student info section, instructions, and questions

### 2. Answer Keys
- **Location**: `Generated_Papers/MCQ/Enhanced/Answers/`
- **Format**: `enhanced_mcq_set_A_answers.pdf`, `enhanced_mcq_set_B_answers.pdf`, etc.
- **Content**: Same layout as question papers but with correct answers highlighted and explanations

### 3. A3 Booklets
- **Location**: `Generated_Papers/MCQ/Enhanced/Booklets/`
- **Format**: `enhanced_mcq_set_A_booklet.pdf`, `enhanced_mcq_set_B_booklet.pdf`, etc.
- **Content**: A3-sized PDFs with pages arranged for booklet printing (two A4 pages per A3 sheet)

### 4. Answer Key CSV
- **Location**: `Generated_Papers/MCQ/Enhanced/enhanced_mcq_answer_keys.csv`
- **Content**: Quick reference table with answers for all sets side-by-side

### 5. Detailed Answer Key JSON
- **Location**: `Generated_Papers/MCQ/Enhanced/enhanced_mcq_answer_keys_detailed.json`
- **Content**: Complete metadata including section info, question numbers, and answers for all sets

## Paper Features

- **Automatic Page Numbering**: Footer shows current page number
- **Two-Column Layout**: Efficient use of space with automatic column balancing
- **Smart Question Placement**: Height estimation ensures questions don't split across pages
- **Student Information Section**: Name, roll number, and instructions (can be disabled with `--no-student-info`)
- **Section Headers**: Clear section names and descriptions
- **End Marker**: Visual indicator showing end of paper
- **Blank Pages for Rough Work**: Automatically added to booklets for page alignment
- **Default Exam Duration**: 120 minutes (shown in header)

## Requirements

- **Python**: 3.7+
- **fpdf2**: PDF generation with Unicode support
- **PyMuPDF**: PDF manipulation for booklet creation
- **google-generativeai**: AI question generation (optional)
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework

See `requirements.txt` for exact versions.

## Examples

### Example 1: Generate Standard Exam

```bash
python enhanced_mcq_paper_builder.py \
  --input-file questions_data/example.json \
  --title "Central High School" \
  --subtitle "Annual Examination 2025" \
  --exam-title "Mathematics - Grade 10"
```

### Example 2: Generate Compact Version with 4 Sets

```bash
python enhanced_mcq_paper_builder.py \
  --input-file questions_data/example.json \
  --num-sets 4 \
  --size small \
  --no-student-info
```

### Example 3: Generate Without Shuffling

```bash
python enhanced_mcq_paper_builder.py \
  --input-file questions_data/example.json \
  --no-shuffle
```

## Sample Files

Check the `questions_data/` folder for examples:
- **`example.json`**: Comprehensive example demonstrating all supported question types
- **`example2.json`**: Additional examples with detailed format demonstrations
- **`test.json`**: Simple test file for quick validation

## Advanced Topics

### Custom Fonts

The system uses three font families:
- **Noto Sans**: Headers and UI elements
- **Arial Unicode**: Question text and options (supports international characters)
- **Stinger Fit**: Title text

Font files are located in the `fonts/` directory.

### Section Configuration

Each section can specify:
- `name`: Section title
- `description`: Instructions or description
- `questions`: Array of question objects
- `required_questions`: Number of questions to include from the pool (optional)

### Shuffling Behavior

When shuffling is enabled (default):
- Questions within each section are shuffled
- Answer options for each question are shuffled
- Different sets get different random orders
- The `--no-shuffle` flag disables all shuffling

### Height Estimation

The generator estimates question height to prevent splitting across pages/columns:
- Calculates text height based on content and font size
- Accounts for special elements (MTF tables, statements, paragraphs)
- Adds safety buffers to prevent overflow
- Automatically moves to next column/page when needed

## Documentation

For more detailed information:
- **Question Format Specs**: See `questions_data/prompt.txt`
- **Enhanced MCQ Details**: See `docs/README_Enhanced_MCQ_Data_Structure.md`
- **Generator Documentation**: See `docs/README_enhancedmcq2.md`

## Contributing

Contributions are welcome! Please ensure:
1. Questions follow the documented JSON structure
2. Test your changes with various question types
3. Check generated PDFs for formatting issues
4. Update documentation as needed

## License

This project is open source. Check the repository for license details.

## Support

For issues, questions, or feature requests, please open an issue on the project repository.
