# PaperGen

A Python-based tool for generating educational question papers in PDF format. Supports both Multiple Choice Questions (MCQ) and mixed-format papers with customizable layouts and formatting.

## Features

- **MCQ Paper Generation**: Create multiple choice question papers with answer keys
- **Mixed Paper Generation**: Generate papers with various question types
- **PDF Output**: Professional PDF generation with proper formatting
- **Customizable Templates**: Flexible configuration for different paper formats
- **Multiple Sets**: Generate multiple paper sets (A, B, etc.) with shuffled questions
- **Answer Keys**: Automatic generation of answer keys and detailed explanations
- **Image Support**: Include images in questions
- **Font Support**: Multiple font options including Arial Unicode and Noto Sans

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### MCQ Paper Generation

```bash
python mcq_paper_builder.py --config path/to/config.json --questions path/to/questions.json
```

### Mixed Paper Generation

```bash
python mixed_paper_builder.py --config path/to/config.json --questions path/to/questions.json
```

### Command Line Options

- `--config`: Path to configuration JSON file
- `--questions`: Path to questions JSON file
- `--output-dir`: Output directory for generated papers
- `--no-shuffle`: Disable question shuffling
- `--sets`: Number of paper sets to generate

## File Structure

- `mcq_paper_builder.py`: Main script for MCQ paper generation
- `mixed_paper_builder.py`: Main script for mixed paper generation
- `paper_generators/`: Core paper generation modules
  - `base_generator.py`: Base generator class
  - `mcq_generator.py`: MCQ-specific generator
  - `mixed_generator.py`: Mixed paper generator
  - `styles.py`: Styling and formatting utilities
- `questions_data/`: Sample question data files
- `fonts/`: Font files for PDF generation
- `Generated_Papers/`: Output directory for generated PDFs

## Question Format

Questions should be stored in JSON format. See `questions_data/` for examples.

### MCQ Questions Format
```json
{
  "questions": [
    {
      "question": "What is the capital of France?",
      "options": ["London", "Berlin", "Paris", "Madrid"],
      "correct_answer": "Paris",
      "explanation": "Paris is the capital city of France."
    }
  ]
}
```

### Mixed Questions Format
```json
{
  "sections": [
    {
      "title": "Section A",
      "questions": [
        {
          "question": "Explain the process of photosynthesis.",
          "marks": 5,
          "type": "essay"
        }
      ]
    }
  ]
}
```

## Configuration

Paper generation can be customized through JSON configuration files. Configure:
- Paper title and subtitle
- Font sizes and styles
- Page layout and spacing
- Section formatting
- Answer key generation options

## Output

Generated papers are saved in the `Generated_Papers/` directory:
- `MCQ/`: MCQ papers, answer keys, and booklets
- `Mixed/`: Mixed format papers and booklets

## Requirements

- Python 3.7+
- fpdf==1.7.2
- PyMuPDF==1.25.3
- Pillow==11.1.0
- Other dependencies listed in requirements.txt