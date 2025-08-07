# Enhanced MCQ Generator - Data Structure Documentation

## Overview

The Enhanced MCQ Generator now supports **advanced statement-based questions** with flexible labeling and multiple statement configurations, plus all existing question types. This update enables sophisticated examination papers with various statement formats commonly used in competitive exams and academic assessments.

## Key Enhancements

- **🆕 Enhanced STATEMENTS Structure**: Support for multiple statements with custom labels
- **🔄 Dual Keyword Support**: Both `"STATEMENT"` and `"STATEMENTS"` keywords work
- **📝 Flexible Labels**: Statement-1/2, Assertion/Reasoning, Assertion/Reasoning/Inference
- **⬅️ Backward Compatible**: Existing single statement format still works
- **🎯 Universal Renderer**: Array-based question_text processing for all types

## Supported Question Types

1. **MCQ** - Standard Multiple Choice Questions
2. **S-MCQ** - Statement-based MCQ (Enhanced with multiple statement support)  
3. **MS-MCQ** - Multiple Statement MCQ (List-based)
4. **MTF-MCQ** - Match the Following MCQ
5. **SEQ-MCQ** - Sequencing MCQ  
6. **P-MCQ** - Paragraph-based MCQ

## Question Text Array Format

### New Array Format (Recommended)
```json
"question_text": ["Context/setup text", "Actual question"]
```

### Legacy String Format (Still Supported)
```json
"question_text": "Single question text"
```

The array format allows you to separate:
- **First element**: Contextual setup or introductory text
- **Second element**: The specific question after type-specific content

## Question Type Structures

### 1. Standard MCQ (`mcq`)

```json
{
  "question_type": "mcq",
  "question_text": [
    "Consider the following programming languages and their typical use cases.",
    "Which programming language is primarily used for web frontend development?"
  ],
  "choices": ["Python", "JavaScript", "C++", "Java"],
  "answer": "JavaScript",
  "reasoning": "JavaScript is the primary language for client-side web development."
}
```

**Rendering Flow:**
1. Context text
2. Actual question  
3. Answer choices

### 2. Statement MCQ (`s-mcq`) - ENHANCED 🆕

The statement MCQ type now supports multiple formats:

#### Single Statement Format (Backward Compatible)
```json
{
  "question_text": [
    "Read the statement below carefully and determine its accuracy.",
    "STATEMENT",
    "Based on your knowledge of Python programming language, evaluate the statement."
  ],
  "statements": [
    {
      "label": "Statement",
      "text": "Python is an interpreted programming language that supports object-oriented programming."
    }
  ],
  "choices": ["The statement is completely true", "The statement is partially true", "The statement is completely false", "Cannot be determined"],
  "answer": "The statement is completely true",
  "reasoning": "Python is indeed an interpreted language and fully supports object-oriented programming paradigms."
}
```

#### Multiple Statements Format (Statement-1, Statement-2)
```json
{
  "question_text": [
    "Consider the following statements about artificial intelligence and machine learning.",
    "STATEMENTS",
    "Evaluate the relationship between these statements."
  ],
  "statements": [
    {
      "label": "Statement-1",
      "text": "Machine Learning is a subset of Artificial Intelligence."
    },
    {
      "label": "Statement-2",
      "text": "Deep Learning is a subset of Machine Learning that uses neural networks."
    }
  ],
  "choices": [
    "Both statements are true and Statement-2 explains Statement-1",
    "Both statements are true but Statement-2 does not explain Statement-1", 
    "Statement-1 is true but Statement-2 is false",
    "Both statements are false"
  ],
  "answer": "Both statements are true but Statement-2 does not explain Statement-1"
}
```

#### Assertion-Reasoning Format
```json
{
  "question_text": [
    "Analyze the following statements about global climate patterns.",
    "STATEMENTS",
    "Determine the correctness of the assertion and reasoning."
  ],
  "statements": [
    {
      "label": "Assertion",
      "text": "The equatorial regions receive more solar radiation than the polar regions."
    },
    {
      "label": "Reasoning",
      "text": "The sun's rays hit the equatorial regions more directly while hitting the polar regions at an oblique angle."
    }
  ],
  "choices": [
    "Both assertion and reasoning are correct, and reasoning explains the assertion",
    "Both assertion and reasoning are correct, but reasoning does not explain the assertion",
    "Assertion is correct but reasoning is incorrect", 
    "Both assertion and reasoning are incorrect"
  ],
  "answer": "Both assertion and reasoning are correct, and reasoning explains the assertion"
}
```

#### Complex Analysis Format (Assertion, Reasoning, Inference)
```json
{
  "question_text": [
    "Evaluate the following statements about chemical bonding and molecular structure.",
    "STATEMENTS",
    "Assess the logical relationship between assertion, reasoning, and inference."
  ],
  "statements": [
    {
      "label": "Assertion",
      "text": "Covalent bonds are stronger than ionic bonds in most cases."
    },
    {
      "label": "Reasoning", 
      "text": "Covalent bonds involve direct sharing of electrons between atoms, creating stronger attractions."
    },
    {
      "label": "Inference",
      "text": "Therefore, covalent compounds have higher melting points than ionic compounds."
    }
  ],
  "choices": [
    "Assertion and reasoning are correct, but inference is incorrect",
    "Assertion is correct, reasoning and inference are incorrect",
    "All three statements are correct and logically connected",
    "All three statements are incorrect"
  ],
  "answer": "Assertion and reasoning are correct, but inference is incorrect"
}
```

**Enhanced Rendering Flow:**
1. Context text
2. Multiple labeled statements (each with custom label: "Statement:", "Assertion:", etc.)
3. Evaluation instruction
4. Answer choices

**Supported Keywords:**
- `"STATEMENT"` - Single statement (backward compatible)  
- `"STATEMENTS"` - Multiple statements with custom labels

### 3. Multiple Statement MCQ (`ms-mcq`) - LIST Format

Questions with multiple correct options using roman numerals (consolidated from old statements format).

```json
{
  "question_text": [
    "Review the following statements about Git version control system.",
    "LIST", 
    "Select the option that identifies all the correct statements."
  ],
  "list_items": [
    "i. Git is a distributed version control system",
    "ii. Git was created by Linus Torvalds",
    "iii. Git requires a central server to function", 
    "iv. Git can track changes in binary files"
  ],
  "choices": ["i and ii only", "i, ii and iv only", "i, ii and iii only", "All statements are correct"],
  "answer": "i, ii and iv only",
  "reasoning": "Git is distributed (i), created by Linus Torvalds (ii), does NOT require a central server (iii is false), and can track binary files (iv)."
}
```

**Rendering Flow:**
1. Context text
2. Multiple list items (i, ii, iii, iv)  
3. Selection instruction
4. Answer choices

**Keywords:** `"LIST"` (unified with sequence questions)

### 4. Match the Following MCQ (`mtf-mcq`)

```json
{
  "question_type": "mtf-mcq",
  "question_text": [
    "Match each programming language with its primary use case.",
    "How many of the following programming languages are correctly matched with their primary use?"
  ],
  "mtf_data": {
    "left_column": [
      "i. Python",
      "ii. JavaScript", 
      "iii. SQL"
    ],
    "right_column": [
      "Data science and AI",
      "Web frontend development",
      "Database queries"
    ]
  },
  "choices": ["Only i and ii", "Only ii and iii", "All three", "None"],
  "answer": "All three",
  "reasoning": "All three languages are correctly matched with their primary use cases."
}
```

**Rendering Flow:**
1. Context text
2. MTF table (left column - right column with dashes)
3. Matching question
4. Answer choices

### 5. Sequencing MCQ (`seq-mcq`) - LIST Format

Questions about ordering or sequencing using alphabetical labels (consolidated format).

```json
{
  "question_text": [
    "Consider the standard software development lifecycle (SDLC) phases listed below.",
    "LIST",
    "What is the correct sequence for these software development lifecycle phases?"
  ],
  "list_items": [
    "A. Requirements Analysis",
    "B. Design",
    "C. Implementation", 
    "D. Testing",
    "E. Deployment"
  ],
  "choices": ["A → B → C → D → E", "A → C → B → D → E", "B → A → C → D → E", "A → B → D → C → E"],
  "answer": "A → B → C → D → E",
  "reasoning": "The standard SDLC follows: Requirements Analysis → Design → Implementation → Testing → Deployment."
}
```

**Rendering Flow:**
1. Context text
2. Sequence items (A, B, C, D, E)
3. Sequencing question  
4. Answer choices

**Keywords:** `"LIST"` (unified with multiple statement questions)

### 6. Paragraph MCQ (`p-mcq`)

Questions based on reading comprehension of a given paragraph.

```json
{
  "question_text": [
    "Study the following information about climate change and its causes.",
    "PARAGRAPH", 
    "According to the paragraph, what has been the dominant driver of climate change since the mid-20th century?"
  ],
  "paragraph": "Climate change refers to long-term shifts in global temperatures and weather patterns. While climate variations are natural, scientific evidence shows that human activities, particularly the emission of greenhouse gases like carbon dioxide from burning fossil fuels, have been the dominant driver of climate change since the mid-20th century. The effects include rising sea levels, more frequent extreme weather events, and changes in precipitation patterns.",
  "choices": ["Natural climate variations", "Solar radiation changes", "Human activities", "Ocean currents"],
  "answer": "Human activities",
  "reasoning": "The paragraph explicitly states that human activities, particularly greenhouse gas emissions from burning fossil fuels, have been the dominant driver since the mid-20th century."
}
```

**Rendering Flow:**
1. Context text
2. Paragraph content (indented)
3. Paragraph-based question
4. Answer choices

**Keywords:** `"PARAGRAPH"`

## Keywords Reference

### Enhanced STATEMENTS Keywords  
- `"STATEMENT"` - Single statement (backward compatible)
- `"STATEMENTS"` - Multiple statements with custom labels

### Unified LIST Keyword
- `"LIST"` - List items (for both ms-mcq and seq-mcq)

### Other Keywords
- `"MTF_DATA"` - Match-the-following data  
- `"PARAGRAPH"` - Reading comprehension paragraph

## Statement Label Examples

The enhanced `statements` array supports flexible labeling:

- **Single**: `"Statement"`  
- **Numbered**: `"Statement-1"`, `"Statement-2"`, etc.
- **Assertion-Reasoning**: `"Assertion"`, `"Reasoning"`
- **Complex Analysis**: `"Assertion"`, `"Reasoning"`, `"Inference"`  
- **Custom**: Any descriptive label like `"Hypothesis"`, `"Conclusion"`, etc.

## Complete JSON Structure  

```json
{
  "sections": [
    {
      "name": "Section Name",
      "description": "Section description", 
      "questions": [
        {
          "question_text": ["Context text", "KEYWORD", "Actual question"],
          "choices": ["Option A", "Option B", "Option C", "Option D"],
          "answer": "Correct Answer",
          "reasoning": "Explanation for the answer",
          
          // Enhanced statements structure (s-mcq):
          "statements": [
            {
              "label": "Statement|Statement-1|Assertion|etc",
              "text": "Statement content"  
            }
          ],
          
          // Unified list structure (ms-mcq, seq-mcq):
          "list_items": ["i. Item", "A. Item"],
          
          // Other type-specific fields:
          "mtf_data": {
            "left_column": ["Items"], 
            "right_column": ["Matches"]
          },
          "paragraph": "For p-mcq type"
        }
      ]
    }
  ]
}
```

## Visual Rendering Features

### Enhanced Statement Layout
- Each statement gets its own custom label (e.g., "Statement-1:", "Assertion:", "Reasoning:")  
- Consistent indentation and spacing between multiple statements
- Proper font sizing with labels using smaller bold font (`option_label` size)
- Optimized vertical spacing for compact yet readable layout

### Font Scaling
- Dynamic font sizing based on PDF configuration (small/medium/large)
- Statement labels scale appropriately with overall document size (9pt/10pt/12pt)
- Maintains readability across different paper formats

### Universal Array Processing
- Context/setup text (first array element)
- Keyword-triggered content (STATEMENTS, LIST, MTF_DATA, PARAGRAPH)
- Follow-up question text (subsequent array elements)
- Answer choices with proper spacing

## Backward Compatibility

The system maintains **full backward compatibility**:

- **Legacy single statement**: Old `"statement"` field still works alongside new `"statements"` array
- **Dual keyword support**: Both `"STATEMENT"` and `"STATEMENTS"` keywords supported
- **String format**: `"question_text": "Single question"` automatically converted to array
- **Existing JSON files**: Continue to work without modification
- **Question type detection**: Smart detection based on keywords and data fields

## Usage Example

```python
from paper_generators.enhanced_mcq_generator import EnhancedMCQPaperGenerator  
from config.mcq_config import MCQConfig

# Create configuration
config = MCQConfig(
    title="ABC International School",
    subtitle="Class X - Multi-Type MCQ Paper",
    exam_title="Enhanced Statement Questions", 
    paper_format='A4',
    size_config='small'  # small/medium/large
)

# Create generator
generator = EnhancedMCQPaperGenerator(
    config=config,
    show_answers=False
)

# Load and generate from JSON
sections = load_questions_from_json("questions_data/struct2.json")
generator.generate_from_sections(sections, "enhanced_paper.pdf")
```

## File Structure

```
questions_data/
├── struct2.json                      # Enhanced question data with statements
paper_generators/
├── enhanced_mcq_generator.py         # Main generator with statement support  
├── mcq_generator.py                  # Base generator class
test_struct2_generator.py             # Test script for validation
README_Enhanced_MCQ_Data_Structure.md # This documentation
```

## Migration Guide

### From Legacy Single Statement:
```json
// Old format
{
  "question_text": ["Context", "Question"],
  "statement": "Single statement text"
}

// New format (backward compatible)
{
  "question_text": ["Context", "STATEMENT", "Question"], 
  "statements": [
    {
      "label": "Statement",
      "text": "Single statement text"
    }
  ]
}
```

### To Enhanced Multiple Statements:
```json
// New enhanced format
{
  "question_text": ["Context", "STATEMENTS", "Question"],
  "statements": [
    {
      "label": "Assertion", 
      "text": "Main claim or hypothesis"
    },
    {
      "label": "Reasoning",
      "text": "Supporting rationale or evidence"  
    }
  ]
}
```

This enhanced structure enables creation of sophisticated examination papers with various statement-based question types commonly used in competitive exams, board examinations, and academic assessments.