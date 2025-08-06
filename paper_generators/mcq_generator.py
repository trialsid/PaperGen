from typing import List, Dict, Optional, Tuple
from .base_generator import BasePaperGenerator, PaperConfig
from functools import lru_cache
from .styles import PaperStyles

class MCQConfig(PaperConfig):
    """Configuration specific to MCQ Paper Generator."""
    
    def __init__(self, 
                 title: str = 'Enter School Name (max 60 chars)',
                 subtitle: str = 'Enter Subtitle (max 50 chars)',
                 exam_title: str = 'Enter Exam Title (max 50 chars)',
                 paper_format: str = 'A4',
                 font_paths: Optional[Dict[str, Dict[str, str]]] = None,
                 font_sizes: Optional[Dict[str, int]] = None,
                 spacing: Optional[Dict[str, float]] = None,
                 size_config: str = 'medium',
                 layout: str = 'two-column'):
        
        super().__init__(
            title=title,
            subtitle=subtitle,
            exam_title=exam_title,
            paper_format=paper_format,
            font_paths=font_paths,
            font_sizes=font_sizes,
            spacing=spacing,
            size_config=size_config
        )
        self.layout = layout

class SectionConfig:
    """Configuration class for MCQ Paper Section."""
    
    def __init__(self,
                 name: str,
                 description: str,
                 questions: List[Dict],
                 required_questions: Optional[int] = None,
                 marks_per_question: int = 1):
        
        if not name or not description:
            raise ValueError("Section name and description are required")
            
        if not questions:
            raise ValueError("Section must contain at least one question")
            
        self.name = name
        self.description = description
        self.questions = questions
        self.required_questions = required_questions or len(questions)
        self.marks_per_question = marks_per_question
        
        if self.required_questions > len(questions):
            raise ValueError(f"Required questions ({self.required_questions}) cannot exceed available questions ({len(questions)})")

class MCQPaperGenerator(BasePaperGenerator):
    """MCQ Paper Generator with enhanced formatting and features."""
    
    def __init__(self, 
                 config: Optional[MCQConfig] = None,
                 show_answers: bool = False,
                 title: Optional[str] = None,
                 subtitle: Optional[str] = None,
                 exam_title: Optional[str] = None,
                 paper_format: str = 'A4',
                 question_count: int = 0,
                 strict_ordering: bool = False,
                 show_student_info: bool = True):
        """Initialize MCQ Paper Generator with configuration."""
        
        # Create config if not provided
        if not config and (title or subtitle or exam_title):
            config = MCQConfig(
                title=title or 'School Name',
                subtitle=subtitle or 'Class Test',
                exam_title=exam_title or 'MCQ Examination',
                paper_format=paper_format
            )
        
        super().__init__(
            config=config,
            show_answers=show_answers,
            paper_format=paper_format,
            question_count=question_count,
            strict_ordering=strict_ordering
        )
        
        self.show_student_info = show_student_info  # Store the parameter

    def header(self) -> None:
        """Draw page header."""
        if self.page_no() == 1:
            self._draw_first_page_header()
        else:
            self._draw_subsequent_page_header()

    def _draw_first_page_header(self) -> None:
        """Draw the header for the first page with full school and exam details."""
        # Calculate available width between margins
        available_width = self.w - 20  # 10mm margin on each side
        
        # Get optimal font size for school title
        title_font_size = self._calculate_optimal_font_size(
            self.config.title,
            available_width,
            self.config.font_sizes['title'],
            min_size=16
        )
        
        # School name
        self.set_font('Stinger', 'B', title_font_size)
        self.set_y(PaperStyles.HEADER_SETTINGS['first_page_y'])
        self.cell(0, 10, self.config.title, 0, 1, 'C')

        # Subtitle
        self.set_font('Stinger', 'B', self.config.font_sizes['subtitle'])
        self.cell(0, 10, self.config.subtitle, 0, 1, 'C')

        # Exam title
        self.set_font('Noto', 'I', self.config.font_sizes['exam_title'])
        title_text = self.config.exam_title
        if self.show_answers:
            title_text += ' (ANSWERS)'
        self.cell(0, 10, title_text, 0, 1, 'C')

        # Draw first line below the titles
        first_line_y = self.get_y() + PaperStyles.HEADER_SETTINGS['line_y_offset']
        self.line(10, first_line_y, self.w - 10, first_line_y)

        if self.show_student_info:
            # Student info section
            self.set_draw_color(*PaperStyles.COLORS['light_grey'])  # Light grey
            
            # Name field
            start_y = first_line_y + 5
            self.set_font('Noto', '', PaperStyles.STUDENT_INFO['label_font_size'])
            label_name = "Name:"
            name_width = self.get_string_width(label_name)
            self.set_xy(12, start_y)
            self.cell(name_width, 5, label_name, 0, 0)
            self.line(12 + name_width + 2, start_y + PaperStyles.STUDENT_INFO['line_offset'], self.w/2 - 5, start_y + PaperStyles.STUDENT_INFO['line_offset'])

            # Class and Section fields
            next_y = start_y + PaperStyles.STUDENT_INFO['field_spacing']
            label_class = "Class:"
            class_width = self.get_string_width(label_class)
            label_section = "Section:"
            section_width = self.get_string_width(label_section)
            
            line_length = 25
            
            self.set_xy(12, next_y)
            self.cell(class_width, 5, label_class, 0, 0)
            class_line_end = 12 + class_width + 2 + line_length
            self.line(12 + class_width + 2, next_y + PaperStyles.STUDENT_INFO['line_offset'], class_line_end, next_y + PaperStyles.STUDENT_INFO['line_offset'])
            
            section_x = class_line_end + 5
            self.set_xy(section_x, next_y)
            self.cell(section_width, 5, label_section, 0, 0)
            self.line(section_x + section_width + 2, next_y + PaperStyles.STUDENT_INFO['line_offset'], 
                    self.w/2 - 5, next_y + PaperStyles.STUDENT_INFO['line_offset'])
            
            # Roll Number field
            roll_y = next_y + PaperStyles.STUDENT_INFO['field_spacing']
            label_roll = "Roll no.:"
            roll_width = self.get_string_width(label_roll)
            
            self.set_xy(12, roll_y)
            self.cell(roll_width, 5, label_roll, 0, 0)
            self.line(12 + roll_width + 2, roll_y + PaperStyles.STUDENT_INFO['line_offset'], self.w/2 - 5, roll_y + PaperStyles.STUDENT_INFO['line_offset'])
            
            # Reset draw color to black
            self.set_draw_color(*PaperStyles.COLORS['black'])
            
            student_end_y = roll_y + 5

            # Instructions section
            instructions_x = self.w / 2 + 5
            instructions_width = (self.w / 2) - 15  # Leave margin on right edge
            instructions_y = start_y - 2
            
            self.set_font('Noto', 'B', PaperStyles.INSTRUCTIONS['title_font_size'])
            self.set_xy(instructions_x, instructions_y)
            self.cell(0, 5, "Instructions:", 0, 1)
            instructions_y += 5
            
            self.set_font('Noto', '', PaperStyles.INSTRUCTIONS['text_font_size'])
            instructions = [
                "Fill OMR sheet with blue/black pen.",
                "Fill circles completely.",
                "No stray marks.",
                "Enter Name, Class, Section."
            ]
            
            # Calculate bullet width
            bullet_width = self.get_string_width('• ')
            text_width = instructions_width - bullet_width - 2  # Extra margin
            
            for instruction in instructions:
                self.set_xy(instructions_x, instructions_y)
                self.cell(bullet_width, 5, '•', 0, 0)
                # Use multi_cell for wrapping text instead of single cell
                self.set_xy(instructions_x + bullet_width, instructions_y)
                self.multi_cell(text_width, PaperStyles.INSTRUCTIONS['line_height'], instruction, 0, 'L')
                instructions_y = self.get_y() + 1  # Add small spacing between instructions
            
            instructions_end_y = instructions_y
            split_section_end_y = max(student_end_y, instructions_end_y)
            
            self.line(self.w/2, first_line_y, self.w/2, split_section_end_y + 2)
            second_line_y = split_section_end_y + 2
        else:
            # Skip student info and instructions, just add a small gap
            second_line_y = first_line_y + 1  # Reduced from 10 to 1
            
        # Draw second horizontal line (above SET info)
        self.line(10, second_line_y, self.w - 10, second_line_y)

        set_name_height = 10
        vertical_gap = 1
        set_name_y = second_line_y + vertical_gap
        third_line_y = set_name_y + set_name_height + vertical_gap

        # Left side - SET name section
        self.set_font('Noto', 'B', self.config.font_sizes['header'])
        self.set_y(set_name_y)
        self.set_x(10)
        self.cell(7, 10, 'SET', 0, 0, 'L')
        self.set_font('Stinger', 'B', 28)
        self.cell(20, 10, f' {self.set_name}', 0, 0, 'L')
        
        # Right side - Total Questions and Duration info
        right_side_width = (self.w/2) - 15
        right_side_start = self.w*0.78
        
        # Create a table structure with two columns
        labels = ['Questions:', 'Duration:']
        values = [f'{self.question_count}', '45min']
        
        # Calculate required column widths
        self.set_font('Noto', '', 10)
        max_label_width = max(self.get_string_width(label) for label in labels)
        
        # Add some padding to the label width
        label_column_width = max_label_width + 5
        value_column_width = right_side_width - label_column_width
        
        # Position to align with the right edge
        right_align_start = right_side_start + right_side_width - label_column_width - value_column_width
        
        # Draw each row of the table
        for i, (label, value) in enumerate(zip(labels, values)):
            row_y = set_name_y + (i * 5)
            
            # Label cell (right aligned)
            self.set_xy(right_align_start, row_y)
            self.set_font('Noto', '', 10)
            self.cell(label_column_width, 5, label, 0, 0, 'R')
            
            # Value cell (left aligned)
            self.set_font('Noto', 'B', 10)
            self.cell(value_column_width, 5, value, 0, 1, 'L')

        self.line(10, third_line_y, self.w - 10, third_line_y)
        # Add a second line right below the third line to create a double-line effect
        self.line(10, third_line_y + 1, self.w - 10, third_line_y + 1)
        self.first_page_offset = third_line_y + 1  # Adjust the offset to account for the additional line
        question_area_end_y = self.h - 12
        self.line(self.w / 2, third_line_y, self.w / 2, question_area_end_y)
        self.set_xy(10, self.first_page_offset + 5)

    def _draw_subsequent_page_header(self) -> None:
        """Draw simplified header for subsequent pages."""
        header_y = PaperStyles.HEADER_SETTINGS['subsequent_page_y']
        self.first_page_offset = 0
        
        self.set_y(header_y)
        
        # For pages 2, 4, 6, etc. (even), use normal positioning
        # For pages 3, 5, 7, etc. (odd but not page 1), flip positions
        should_flip = self.page_no() % 2 != 0
        
        self.set_font('Noto', 'B', self.config.font_sizes['header'])
        exam_title = self.config.exam_title
        if self.show_answers:
            exam_title += " - Answer Key"
        left_text = exam_title
        right_text = self.config.title
        
        # Render the left side
        self.set_x(10)
        self.cell((self.w/2) - 15, 10, 
                right_text if should_flip else left_text, 
                0, 0, 'L')
        
        # Render the right side
        self.set_x(self.w/2 + 5)
        self.cell((self.w/2) - 15, 10, 
                left_text if should_flip else right_text, 
                0, 0, 'R')
        
        self.line(10, header_y + 10, self.w - 10, header_y + 10)
        self.line(self.w/2, header_y + 10, self.w/2, self.h - 12)
        self.set_xy(10, header_y + 15)

    def footer(self) -> None:
        self.line(10, self.h - 12, self.w - 10, self.h - 12)
        self.set_y(-10)
        self.set_font('Noto', 'I', self.config.font_sizes['footer'])
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')
    
    @lru_cache(maxsize=1024)
    def get_cached_string_width(self, text: str, font_family: str, font_style: str, font_size: int) -> float:
        self.set_font(font_family, font_style, font_size)
        return self.get_string_width(text)
    
    def measure_option_width(self, option_text: str) -> float:
        return self.get_cached_string_width(
            f"A. {option_text}",
            'ArialUni',
            '',
            self.config.font_sizes['option']
        )
    
    def can_fit_two_options(self, option1: str, option2: str) -> bool:
        width1 = self.measure_option_width(option1)
        width2 = self.measure_option_width(option2)
        total_width = width1 + width2 + self.config.spacing['option_column_gap']
        return total_width <= self._options_width
    
    def write_option(self, label: str, option_text: str, x: float, y: float, 
                    width: float, is_answer: bool = False) -> float:
        """Write a single option and return its height."""
        # Calculate height needed for this option first
        option_height = self.estimate_text_height(
            f"{label} {option_text}", 
            width, 
            self.config.font_sizes['option']
        )
        
        # Check if we have enough space for this complete option
        footer_buffer = self.MIN_FOOTER_BUFFER + 2
        if (y + option_height) > (self.h - footer_buffer):
            return -1  # Return -1 to indicate insufficient space
            
        # Calculate vertical offset to align baseline of different fonts
        label_font_size = self.config.font_sizes['option_label']
        option_font_size = self.config.font_sizes['option']
        
        # Determine font metrics to align baselines
        # Typically, font baseline is approximately at 80% of font height
        label_font_height = label_font_size * 0.352778  # Convert pt to mm (1 pt = 0.352778 mm)
        option_font_height = option_font_size * 0.352778  # Convert pt to mm
        
        # Set position for label
        self.set_xy(x, y)
        label_width = 5
        self.set_font('Noto', 'B', label_font_size)
        self.cell(label_width, 5, label, 0, 0)
        
        # Calculate y offset for option text to align with label baseline
        self.set_xy(x + label_width, y)
        
        # Set font for option text
        if is_answer and self.show_answers:
            self.set_font('ArialUni', 'B', option_font_size)
            option_text = option_text + " *"
        else:
            self.set_font('ArialUni', '', option_font_size)
            
        # Write the option text aligned with label
        self.multi_cell(width - label_width + 1, self.config.spacing['line_height'], option_text, align='L')
        return self.get_y() - y
    
    def write_option_pair(self, options: List[Tuple[str, str, bool]], start_idx: int, 
                         x: float, y: float, width: float) -> float:
        """Write two options side by side and return the maximum height."""
        if start_idx >= len(options):
            return 0

        half_width = (width - self.config.spacing['option_column_gap']) / 2
        label1, text1, is_answer1 = options[start_idx]
        
        # Check space for first option
        height1 = self.write_option(label1, text1, x, y, half_width, is_answer1)
        if height1 == -1:  # Insufficient space
            return -1
        
        height2 = 0
        if start_idx + 1 < len(options):
            label2, text2, is_answer2 = options[start_idx + 1]
            x2 = x + half_width + self.config.spacing['option_column_gap']
            height2 = self.write_option(label2, text2, x2, y, half_width, is_answer2)
            if height2 == -1:  # Insufficient space for second option
                return -1
        
        return max(height1, height2)
    
    def _write_single_option(self, label: str, option_text: str, x: float, y: float, 
                            width: float, is_answer: bool = False) -> float:
        """Write a single option and return its height."""
        # Set position for label - use same line height as option text
        self.set_xy(x, y)
        label_width = 5
        self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
        self.cell(label_width, self.config.spacing['line_height'], label, 0, 0)
        
        # Set position for option text at same baseline
        self.set_xy(x + label_width, y)
        
        # Set font for option text
        if is_answer and self.show_answers:
            self.set_font('ArialUni', 'B', self.config.font_sizes['option'])
            option_text = option_text + " *"
        else:
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            
        # Write the option text
        self.multi_cell(width - label_width + 1, self.config.spacing['line_height'], option_text, align='L')
        return self.get_y() - y
    
    def _move_to_next_position(self):
        """Move to next column or page when current position has insufficient space."""
        if self.current_side == 'left':
            # Try right column
            right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
            self.current_side = 'right'
            self.set_xy(self.w/2 + 2, right_column_start)
        else:
            # Already on right side, start new page
            self.add_page()
            self.current_side = 'left'
            self.set_xy(10, 20)
    
    @lru_cache(maxsize=1024)
    def estimate_text_height(self, text: str, width: float, font_size: int = 12) -> float:
        self.set_font('Noto', '', font_size)
        words = text.split()
        lines = 1
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            if self.get_string_width(test_line) > width:
                lines += 1
                current_line = word
            else:
                current_line = test_line
        
        return lines * self.config.spacing['line_height']

    def add_question(self, number: int, question_text: str, choices: List[str], 
                    correct_answer_index: Optional[int] = None, reasoning: Optional[str] = None) -> None:
        """Add a question with its options, ensuring they stay together."""
        # This is a complete rewrite to fix the option splitting issue
        
        # Calculate actual height needed more accurately
        needed_height = self.measure_question_height(question_text, choices, reasoning)
        safety_buffer = 5  # Keep reasonable buffer
        total_needed_height = needed_height + safety_buffer
        
        # Get current position and effective page bounds
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        
        # Calculate available space in current position
        available_space = effective_page_height - current_y
        
        # If not enough space, move to next column or page BEFORE writing anything
        if total_needed_height > available_space:
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    # Move to right column
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    # Need new page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                # Already on right side, need new page
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            # Now call recursively with better positioning
            return self.add_question(number, question_text, choices, correct_answer_index, reasoning)
        
        # Now we have confirmed space - write the question
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # Write question number and text
        self.set_font('Noto', 'B', self.config.font_sizes['question_number'])
        self.set_xy(x_start, start_y)
        self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
        
        question_x = x_start + self.config.spacing['question_number_width'] + 1
        self.set_xy(question_x, start_y)
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        self.multi_cell(self._question_width, self.config.spacing['line_height'], question_text)
        
        # Write options - use intelligent pairing when possible
        options_x = question_x + 2
        current_y = self.get_y() + 1
        i = 0
        
        while i < len(choices):
            # Check if we can fit two options side by side
            if (i + 1 < len(choices) and 
                self.can_fit_two_options(choices[i], choices[i+1])):
                # Write two options side by side
                half_width = (self._options_width - self.config.spacing['option_column_gap']) / 2
                
                # First option
                label1 = f"{chr(65+i)}."
                is_answer1 = (i == correct_answer_index)
                option_height1 = self._write_single_option(
                    label1, choices[i], options_x, current_y, half_width, is_answer1
                )
                
                # Second option  
                label2 = f"{chr(65+i+1)}."
                is_answer2 = (i+1 == correct_answer_index)
                x2 = options_x + half_width + self.config.spacing['option_column_gap']
                option_height2 = self._write_single_option(
                    label2, choices[i+1], x2, current_y, half_width, is_answer2
                )
                
                current_y += max(option_height1, option_height2) + 1
                i += 2
            else:
                # Write single option
                label = f"{chr(65+i)}."
                is_answer = (i == correct_answer_index)
                option_height = self._write_single_option(
                    label, choices[i], options_x, current_y, self._options_width, is_answer
                )
                current_y += option_height + 1
                i += 1
        
        # Add reasoning if needed
        if reasoning and self.show_answers:
            current_y += 1
            self.set_xy(options_x, current_y)
            self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
            self.cell(30, 5, "Explanation:", 0, 0)
            
            self.set_xy(options_x, current_y + 5)
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            self.multi_cell(self._options_width, self.config.spacing['line_height'], reasoning)
            current_y = self.get_y() + 2
        
        # Set final position
        self.set_y(current_y + 1)

    def measure_question_height(self, question_text: str, choices: List[str], reasoning: Optional[str] = None) -> float:
        """Calculate the height needed for a question and its options."""
        # Calculate question text height with minimal padding
        question_height = self.estimate_text_height(
            question_text, 
            self._question_width, 
            self.config.font_sizes['question']
        )
        
        # Add very minimal spacing after question
        total_height = question_height + 1  # Reduced from 1.5 to 1
        
        half_options_width = (self._options_width/2) - 1  # Reduced from 1.5 to 1
        
        # Calculate options height with very minimal padding
        i = 0
        while i < len(choices):
            if i + 1 < len(choices) and self.can_fit_two_options(choices[i], choices[i+1]):
                # For side-by-side options, calculate max height with very minimal padding
                height = max(
                    self.estimate_text_height(
                        f"A. {choices[i]}", 
                        half_options_width, 
                        self.config.font_sizes['option']
                    ),
                    self.estimate_text_height(
                        f"B. {choices[i+1]}", 
                        half_options_width, 
                        self.config.font_sizes['option']
                    )
                ) + 0.1  # Reduced from 0.25 to 0.1
                total_height += height
                i += 2
                continue
            
            # For single options, add very minimal padding
            option_height = self.estimate_text_height(
                f"A. {choices[i]}", 
                self._options_width, 
                self.config.font_sizes['option']
            ) + 0.1  # Reduced from 0.25 to 0.1
            
            total_height += option_height
            i += 1
            total_height += 0.5  # Reduced from 0.75 to 0.5
        
        # Add height for reasoning if available and we're showing answers
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}",
                self._options_width,
                self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7  # Extra space for the explanation label and padding
        
        # Add a very minimal buffer for safety
        buffer_space = 2  # Reduced from 3 to 2
        return total_height + buffer_space

    def check_and_adjust_position(self, needed_height: float, questions: List[Dict], current_idx: int) -> Tuple[bool, int]:
        """Check if there's enough space for content and adjust position if needed."""
        current_y = self.get_y()
        # Use a very minimal footer buffer
        footer_buffer = self.MIN_FOOTER_BUFFER + 2  # Reduced from 3 to 2
        effective_page_height = self.h - footer_buffer
        
        # Calculate available space from current position
        if self.page_no() == 1:
            start_y = max(current_y, self.first_page_offset + 5)
        else:
            start_y = current_y
        
        # If current position doesn't have enough space for the entire question
        if (current_y + needed_height) > effective_page_height:
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_column_space = effective_page_height - right_column_start
                
                # Use a very minimal safety margin
                safety_margin = 1  # Reduced from 2 to 1
                if (right_column_space - safety_margin) >= needed_height:
                    # Move to right column if there's enough space
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    # If right column can't fit, create new page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                # If we're already on right side, always start new page
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
        
        return True, current_idx

    def generate_from_sections(self, sections: List[SectionConfig]) -> int:
        """Generate MCQ paper from sectioned data and return total marks."""
        question_number = 1
        total_marks = 0
        
        for section in sections:
            # Use exactly the questions provided, limited to required_questions count
            selected_questions = section.questions[:section.required_questions]
            
            # Add question numbers and prepare question data
            questions_with_numbers = []
            for q in selected_questions:
                q_data = q.copy()
                q_data['number'] = question_number
                questions_with_numbers.append(q_data)
                question_number += 1
            
            # Calculate height of first question to prevent orphaned section header
            first_question = questions_with_numbers[0]
            first_question_height = self.measure_question_height(
                first_question['question'],
                first_question['choices'],
                first_question.get('reasoning')
            )
            
            # Add section header with knowledge of next question's height
            self.add_section(section.name, section.description, first_question_height)
            
            # Write the first question immediately after the section header without position adjustment
            self.add_question(
                first_question['number'],
                first_question['question'],
                first_question['choices'],
                first_question['choices'].index(first_question['answer']) if self.show_answers else None,
                first_question.get('reasoning') if self.show_answers and 'reasoning' in first_question else None
            )
            
            # Add the remaining questions for this section with space optimization
            current_idx = 1  # Start from the second question
            while current_idx < len(questions_with_numbers):
                question = questions_with_numbers[current_idx]
                needed_height = self.measure_question_height(
                    question['question'],
                    question['choices'],
                    question.get('reasoning')
                )
                
                # Only adjust position if not using strict ordering
                if not self.strict_ordering:
                    _, new_idx = self.check_and_adjust_position(
                        needed_height,
                        questions_with_numbers[current_idx:],
                        0
                    )
                    
                    # Get potentially reordered question
                    question = questions_with_numbers[current_idx]
                else:
                    # With strict ordering, just check if we need to adjust position
                    success, _ = self.check_and_adjust_position(needed_height, [], 0)
                    if not success:
                        continue
                
                self.add_question(
                    question['number'],
                    question['question'],
                    question['choices'],
                    question['choices'].index(question['answer']) if self.show_answers else None,
                    question.get('reasoning') if self.show_answers and 'reasoning' in question else None
                )
                
                current_idx += 1
                total_marks += section.marks_per_question
        
        # Add styled "END" text with gradient-colored asterisks
        self.draw_end_marker()
        
        # Update total marks in the header if this is the first page
        if hasattr(self, 'question_count'):
            self.question_count = question_number - 1
            
        return total_marks 