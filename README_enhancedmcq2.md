# Enhanced MCQ JSON Data Structure

This document describes the JSON structure used by the Enhanced MCQ Generator for creating multiple-choice question papers. The structure supports various question types including standard MCQ, statement evaluation, list-based questions, match-the-following (MTF), and paragraph-based questions.

## Root Structure

```json
{
  "sections": [
    {
      "name": "Section Name",
      "description": "Section description",
      "questions": [...]
    }
  ]
}
```

## Question Text Formatting

The `question_text` field supports flexible formatting:

- **Single string**: `"question_text": "Single line question"`
- **Multiple strings**: `"question_text": ["Line 1", "Line 2", "Line 3"]`

When using an array, each string is rendered on a new line. Use multiple strings when you want line breaks between sentences or sections. Use a single string when no line breaks are needed.

## Question Types

### 1. Standard Multiple Choice Question (MCQ)

Simple MCQ with single line:
```json
{
  "question_text": ["What is the capital of France?"],
  "choices": ["London", "Paris", "Berlin", "Madrid"],
  "answer": "Paris",
  "reasoning": "Paris is the capital and largest city of France"
}
```

MCQ with multiple lines (each string renders on new line):
```json
{
  "question_text": [
    "Consider the following programming concepts.",
    "Which language is primarily used for web frontend development?"
  ],
  "choices": ["Python", "JavaScript", "C++", "Java"],
  "answer": "JavaScript",
  "reasoning": "JavaScript runs in browsers for interactive user interfaces"
}
```

### 2. Statement Evaluation Question

**Variation 1 - Simple intro + keyword + outro:**
```json
{
  "question_text": [
    "Consider the following statement about web development:",
    "STATEMENT",
    "Is this statement accurate?"
  ],
  "statements": [
    {
      "label": "Statement",
      "text": "CSS Grid Layout is better than Flexbox for all layout scenarios."
    }
  ],
  "choices": ["Completely true", "Partially true", "Completely false", "Cannot be determined"],
  "answer": "Completely false",
  "reasoning": "CSS Grid and Flexbox serve different purposes - Grid for 2D layouts, Flexbox for 1D layouts."
}
```

**Variation 2 - Multiple intro blocks + keyword:**
```json
{
  "question_text": [
    "In modern database design, there are various approaches to data modeling.",
    "Each approach has its own advantages and use cases.",
    "STATEMENT",
    "Evaluate this claim:"
  ],
  "statements": [
    {
      "label": "Statement", 
      "text": "NoSQL databases are always faster than relational databases for all types of queries."
    }
  ],
  "choices": ["Always true", "Sometimes true", "Never true", "Depends on use case"],
  "answer": "Never true",
  "reasoning": "Performance depends on data structure, query patterns, and specific use cases - neither is universally faster."
}
```

**Variation 3 - Keyword only:**
```json
{
  "question_text": [
    "STATEMENT"
  ],
  "statements": [
    {
      "label": "Statement",
      "text": "Machine learning algorithms can completely replace human judgment in all decision-making scenarios."
    }
  ],
  "choices": ["True", "False", "Partially true", "Context dependent"],
  "answer": "False",
  "reasoning": "ML algorithms have limitations and biases; human oversight remains crucial for many decisions."
}
```

### 3. List-Based Question

**Variation 1 - Context + keyword + instruction:**
```json
{
  "question_text": [
    "Cloud computing has revolutionized how businesses deploy applications.",
    "LIST",
    "Which of these statements about cloud services are accurate?"
  ],
  "list_items": [
    "i. SaaS provides software over the internet",
    "ii. PaaS includes operating system management", 
    "iii. IaaS offers the highest level of control",
    "iv. All cloud services require internet connectivity"
  ],
  "choices": ["i and iii only", "i, iii and iv only", "ii and iv only", "All statements"],
  "answer": "i, iii and iv only",
  "reasoning": "SaaS is software-as-service (i✓), PaaS abstracts OS management (ii✗), IaaS gives full control (iii✓), all need internet (iv✓)."
}
```

**Variation 2 - Multiple context blocks + keyword:**
```json
{
  "question_text": [
    "Cybersecurity is a critical concern in today's digital world.",
    "Various techniques are used to protect systems and data.",
    "However, not all security practices are equally effective.",
    "LIST"
  ],
  "list_items": [
    "a) Two-factor authentication adds an extra security layer",
    "b) Using the same password across multiple sites is convenient",
    "c) Regular software updates patch security vulnerabilities", 
    "d) Public Wi-Fi is safe for all online activities"
  ],
  "choices": ["a and c only", "a, b and c", "b and d only", "a, c and d"],
  "answer": "a and c only",
  "reasoning": "2FA improves security (a✓), same passwords are risky (b✗), updates fix vulnerabilities (c✓), public Wi-Fi is insecure (d✗)."
}
```

**Variation 3 - Keyword + detailed instruction:**
```json
{
  "question_text": [
    "LIST",
    "Examine these programming concepts and identify which ones are correctly described:",
    "Mark your answer based on technical accuracy."
  ],
  "list_items": [
    "1. Recursion always uses less memory than iteration",
    "2. Binary search works only on sorted arrays",
    "3. Hash tables provide O(1) average-case lookup time",
    "4. Linked lists allow random access to elements"
  ],
  "choices": ["2 and 3 only", "1 and 4 only", "2, 3 and 4", "All are correct"],
  "answer": "2 and 3 only",
  "reasoning": "Recursion uses more memory (1✗), binary search needs sorted data (2✓), hash tables are O(1) average (3✓), linked lists are sequential access (4✗)."
}
```

### 4. Match-the-Following (MTF) Question

**Variation 1 - Simple intro + keyword:**
```json
{
  "question_text": [
    "Test your knowledge of network protocols:",
    "MTF_DATA"
  ],
  "mtf_data": {
    "left_column": [
      "A. HTTP",
      "B. FTP", 
      "C. SMTP",
      "D. DNS"
    ],
    "right_column": [
      "File Transfer",
      "Domain Name Resolution", 
      "Web Communication",
      "Email Delivery"
    ]
  },
  "choices": ["All correct", "3 out of 4", "2 out of 4", "1 out of 4"],
  "answer": "All correct",
  "reasoning": "HTTP-Web (A✓), FTP-File Transfer (B✓), SMTP-Email (C✓), DNS-Domain Resolution (D✓)."
}
```

**Variation 2 - Context building + keyword + question:**
```json
{
  "question_text": [
    "In software architecture, different design patterns solve specific problems.",
    "Each pattern has its own structure and use case.",
    "MTF_DATA",
    "How many patterns are correctly matched with their primary purpose?"
  ],
  "mtf_data": {
    "left_column": [
      "1. Singleton",
      "2. Factory",
      "3. Observer"
    ],
    "right_column": [
      "Object creation without specifying exact class",
      "Ensure only one instance exists",
      "Notify multiple objects about state changes"
    ]
  },
  "choices": ["All three", "Only 1 and 2", "Only 2 and 3", "None"],
  "answer": "All three", 
  "reasoning": "Singleton ensures one instance (1✓), Factory creates objects abstractly (2✓), Observer notifies dependents (3✓)."
}
```

**Variation 3 - Direct keyword + multiple instructions:**
```json
{
  "question_text": [
    "MTF_DATA",
    "Match the data structures with their time complexities.",
    "Consider average-case scenarios for your matching."
  ],
  "mtf_data": {
    "left_column": [
      "i. Array access",
      "ii. Binary search tree search",
      "iii. Hash table lookup",
      "iv. Linked list search"
    ],
    "right_column": [
      "O(n)",
      "O(1)", 
      "O(log n)",
      "O(1)"
    ]
  },
  "choices": ["2 matches correct", "3 matches correct", "All matches correct", "No matches correct"],
  "answer": "3 matches correct",
  "reasoning": "Array access O(1) (i✓), BST search O(log n) (ii✓), Hash lookup O(1) (iii✓), Linked search O(n) (iv✗)."
}
```

### 5. Multiple Statement Question (Assertion-Reasoning)

**Variation 1 - Brief intro + keyword + evaluation:**
```json
{
  "question_text": [
    "Consider these claims about mobile app development:",
    "STATEMENTS",
    "What's the relationship between them?"
  ],
  "statements": [
    {
      "label": "Assertion",
      "text": "React Native allows developers to build native mobile apps using JavaScript."
    },
    {
      "label": "Reason",
      "text": "React Native compiles JavaScript code directly to native machine code."
    }
  ],
  "choices": [
    "Both correct, reason explains assertion",
    "Both correct, reason doesn't explain assertion", 
    "Assertion correct, reason incorrect",
    "Both incorrect"
  ],
  "answer": "Assertion correct, reason incorrect",
  "reasoning": "React Native does enable native apps with JavaScript (assertion✓), but it uses a bridge to native components, not direct compilation (reason✗)."
}
```

**Variation 2 - Keyword only:**
```json
{
  "question_text": [
    "STATEMENTS"
  ],
  "statements": [
    {
      "label": "Statement-A",
      "text": "Blockchain technology ensures complete data immutability."
    },
    {
      "label": "Statement-B", 
      "text": "Smart contracts eliminate the need for legal agreements."
    }
  ],
  "choices": ["Both true", "A true, B false", "A false, B true", "Both false"],
  "answer": "Both false",
  "reasoning": "Blockchain can be modified through consensus mechanisms (A✗), and smart contracts complement but don't replace legal frameworks (B✗)."
}
```

**Variation 3 - Extended context + keyword:**
```json
{
  "question_text": [
    "In the era of cloud computing, various deployment models have emerged.",
    "Each model offers different levels of control, flexibility, and responsibility.",
    "Understanding these differences is crucial for making informed decisions.",
    "STATEMENTS"
  ],
  "statements": [
    {
      "label": "Claim",
      "text": "Infrastructure as a Service (IaaS) provides the most control over the computing environment."
    },
    {
      "label": "Justification",
      "text": "IaaS users manage the operating system, middleware, and applications while the provider handles physical infrastructure."
    }
  ],
  "choices": [
    "Claim and justification both correct and linked",
    "Both correct but not linked",
    "Claim correct, justification wrong",
    "Both wrong"
  ],
  "answer": "Claim and justification both correct and linked",
  "reasoning": "IaaS indeed provides maximum control (claim✓) because users manage everything above hardware level (justification✓ and explains claim)."
}
```

### 6. Sequence/Ordering Question

**Variation 1 - Context + keyword + question:**
```json
{
  "question_text": [
    "Database transactions must follow specific steps to maintain ACID properties.",
    "LIST",
    "What's the correct sequence for a typical database transaction?"
  ],
  "list_items": [
    "A. Begin Transaction",
    "B. Execute Operations", 
    "C. Commit/Rollback",
    "D. Release Locks"
  ],
  "choices": ["A → B → C → D", "A → B → D → C", "B → A → C → D", "A → C → B → D"],
  "answer": "A → B → C → D",
  "reasoning": "Transaction sequence: Begin → Execute → Commit/Rollback → Release Locks to ensure atomicity and consistency."
}
```

**Variation 2 - Keyword first + instruction:**
```json
{
  "question_text": [
    "LIST",
    "Arrange these HTTP request processing steps in the correct order:"
  ],
  "list_items": [
    "1. Parse request headers",
    "2. Establish TCP connection",
    "3. Send HTTP response",
    "4. Process request body",
    "5. Route to handler"
  ],
  "choices": ["2 → 1 → 4 → 5 → 3", "1 → 2 → 4 → 5 → 3", "2 → 1 → 5 → 4 → 3", "1 → 4 → 2 → 5 → 3"],
  "answer": "2 → 1 → 4 → 5 → 3",
  "reasoning": "HTTP processing: TCP connection → parse headers → process body → route to handler → send response."
}
```

**Variation 3 - Multiple context + keyword + detailed question:**
```json
{
  "question_text": [
    "Machine learning model development involves several critical phases.",
    "Each phase builds upon the previous one and affects overall model performance.", 
    "Proper sequencing ensures effective model training and validation.",
    "LIST",
    "What is the optimal sequence for these ML development phases?"
  ],
  "list_items": [
    "X. Model Training",
    "Y. Data Preprocessing",
    "Z. Feature Engineering", 
    "W. Model Evaluation"
  ],
  "choices": ["Y → Z → X → W", "Z → Y → X → W", "Y → X → Z → W", "X → Y → Z → W"],
  "answer": "Y → Z → X → W",
  "reasoning": "ML workflow: Data Preprocessing → Feature Engineering → Model Training → Model Evaluation for optimal results."
}
```

### 7. Paragraph-Based Question

**Variation 1 - Intro + keyword + specific question:**
```json
{
  "question_text": [
    "Read the following passage about modern web development:",
    "PARAGRAPH",
    "What does the passage identify as the main advantage of microservices architecture?"
  ],
  "paragraph": "Microservices architecture has revolutionized how large-scale applications are built and deployed. Unlike monolithic architectures where all components are tightly coupled, microservices break applications into small, independent services that communicate through APIs. This approach offers several benefits: improved scalability, technology diversity, fault isolation, and faster development cycles. However, it also introduces complexity in service coordination, data consistency, and distributed system management.",
  "choices": ["Technology diversity", "Improved scalability", "Fault isolation", "All of the above"],
  "answer": "All of the above",
  "reasoning": "The passage lists multiple main advantages: scalability, technology diversity, and fault isolation, making all correct."
}
```

**Variation 2 - Keyword only:**
```json
{
  "question_text": [
    "PARAGRAPH"
  ],
  "paragraph": "Artificial intelligence bias occurs when AI systems produce discriminatory results due to prejudiced assumptions in their training data or algorithms. This can manifest in various ways: facial recognition systems performing poorly on certain ethnic groups, hiring algorithms favoring specific demographics, or recommendation systems reinforcing stereotypes. Addressing AI bias requires diverse training datasets, algorithmic auditing, and inclusive development teams. The stakes are high as biased AI can perpetuate and amplify existing social inequalities.",
  "choices": [
    "What causes AI bias according to the passage?",
    "Training data prejudice and algorithmic assumptions", 
    "Poor facial recognition technology",
    "Inadequate computing resources",
    "Insufficient data volume"
  ],
  "answer": "Training data prejudice and algorithmic assumptions",
  "reasoning": "The passage clearly states AI bias stems from 'prejudiced assumptions in their training data or algorithms.'"
}
```

**Variation 3 - Context setup + keyword + analysis question:**
```json
{
  "question_text": [
    "The following passage discusses an important concept in distributed systems.",
    "Pay attention to the trade-offs mentioned.",
    "PARAGRAPH",
    "Based on the passage, what is the fundamental challenge described?"
  ],
  "paragraph": "The CAP theorem, proposed by Eric Brewer, states that any distributed data store can only guarantee two out of three properties: Consistency (all nodes see the same data simultaneously), Availability (system remains operational), and Partition tolerance (system continues despite network failures). This creates a fundamental trade-off in distributed system design. For example, choosing consistency and availability means the system cannot handle network partitions, while choosing availability and partition tolerance means accepting eventual consistency rather than strong consistency.",
  "choices": [
    "Network failures are unavoidable",
    "Systems can only guarantee two of three CAP properties",
    "Distributed systems are too complex",
    "Data storage is inherently unreliable"
  ],
  "answer": "Systems can only guarantee two of three CAP properties",
  "reasoning": "The passage explicitly describes the CAP theorem's fundamental trade-off: only two out of three properties (Consistency, Availability, Partition tolerance) can be guaranteed simultaneously."
}
```

### 8. Complex Multi-Statement Question

**Variation 1 - Standard intro + keyword + evaluation:**
```json
{
  "question_text": [
    "Analyze the following statements about containerization technology:",
    "STATEMENTS",
    "Determine the validity of each statement and their logical connection."
  ],
  "statements": [
    {
      "label": "Statement-1",
      "text": "Docker containers share the host operating system kernel."
    },
    {
      "label": "Statement-2", 
      "text": "This sharing makes containers more lightweight than virtual machines."
    },
    {
      "label": "Statement-3",
      "text": "Therefore, containers always start faster than virtual machines."
    }
  ],
  "choices": [
    "All statements correct and logically connected",
    "Statements 1 and 2 correct, 3 incorrect but follows logically",
    "Only statement 1 correct",
    "All statements incorrect"
  ],
  "answer": "Statements 1 and 2 correct, 3 incorrect but follows logically",
  "reasoning": "Docker containers do share host kernel (1✓) making them lighter than VMs (2✓), but startup speed depends on application complexity, not just containerization (3✗)."
}
```

**Variation 2 - Extended context + keyword:**
```json
{
  "question_text": [
    "Software testing is a critical phase in application development.",
    "Different testing approaches serve different purposes and have varying effectiveness.",
    "Understanding the relationship between testing strategies helps optimize quality assurance.",
    "STATEMENTS"
  ],
  "statements": [
    {
      "label": "Premise",
      "text": "Unit testing focuses on individual components in isolation."
    },
    {
      "label": "Claim",
      "text": "Integration testing becomes unnecessary when unit test coverage is 100%."
    },
    {
      "label": "Conclusion",
      "text": "Teams can skip integration testing if all unit tests pass."
    }
  ],
  "choices": [
    "Premise correct, claim and conclusion incorrect",
    "All statements correct",
    "Only premise correct", 
    "All statements incorrect"
  ],
  "answer": "Premise correct, claim and conclusion incorrect",
  "reasoning": "Unit testing does test components in isolation (premise✓), but integration testing checks component interactions that unit tests miss (claim✗), so integration testing remains necessary (conclusion✗)."
}
```

**Variation 3 - Keyword + post-analysis instructions:**
```json
{
  "question_text": [
    "STATEMENTS",
    "Examine these claims about cybersecurity practices.",
    "Consider both technical accuracy and practical implications."
  ],
  "statements": [
    {
      "label": "Theory",
      "text": "End-to-end encryption ensures that only intended recipients can read messages."
    },
    {
      "label": "Practice",
      "text": "Implementing E2E encryption eliminates all security vulnerabilities in communication systems."
    },
    {
      "label": "Policy",
      "text": "Organizations should rely solely on E2E encryption for secure communications."
    }
  ],
  "choices": [
    "Theory correct, practice and policy flawed",
    "All statements technically sound",
    "Theory and practice correct, policy questionable",
    "Only theory has merit"
  ],
  "answer": "Theory correct, practice and policy flawed",
  "reasoning": "E2E encryption does protect message content (theory✓), but doesn't eliminate metadata leaks, endpoint vulnerabilities, or implementation flaws (practice✗), and requires layered security approach (policy✗)."
}
```

## Special Keywords

The enhanced generator recognizes these special keywords in `question_text` arrays:

- **`STATEMENT`**: Renders the statements section
- **`STATEMENTS`**: Renders multiple statements (assertion/reasoning format)
- **`LIST`**: Renders the list_items as a formatted list
- **`MTF_DATA`**: Renders the match-the-following table
- **`PARAGRAPH`**: Renders the paragraph content

## Required Fields

- `question_text`: Array of strings (can contain special keywords)
- `choices`: Array of answer options
- `answer`: The correct answer (must match one of the choices)
- `reasoning`: Explanation for the correct answer

## Optional Fields

- `statements`: Array of statement objects (for statement-type questions)
- `list_items`: Array of list items (for list-type questions)
- `mtf_data`: Object with left_column and right_column arrays
- `paragraph`: String containing paragraph text

## Section Structure

Each section contains:
- `name`: Section title
- `description`: Section description
- `questions`: Array of question objects

This structure supports flexible question formats while maintaining consistency in rendering and grading.