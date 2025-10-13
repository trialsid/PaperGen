from typing import List, Dict, Optional, Tuple
from .base_generator import BasePaperGenerator, PaperConfig
from .styles import PaperStyles

class MixedConfig(PaperConfig):
    """Configuration specific to Mixed Paper Generator."""
    pass  # Currently using all base config, but can be extended for mixed paper-specific settings

class MixedSectionConfig:
    """Configuration class for Mixed Question Paper Section."""
    
    def __init__(self,
                 name: str,
                 description: str,
                 section_type: str,
                 questions: List[Dict],
                 required_questions: Optional[int] = None):
        
        if not name or not description:
            raise ValueError("Section name and description are required")
            
        if not questions:
            raise ValueError("Section must contain at least one question")
            
        if section_type not in ['MCQ', 'AW', 'FB', 'MTF']:
            raise ValueError("Invalid section type. Must be MCQ, AW, FB, or MTF")
            
        self.name = name
        self.description = description
        self.section_type = section_type
        self.questions = questions
        self.required_questions = required_questions or len(questions)
        
        if self.required_questions > len(questions):
            raise ValueError(f"Required questions ({self.required_questions}) cannot exceed available questions ({len(questions)})")

class MixedPaperGenerator(BasePaperGenerator):
    """Mixed Question Paper Generator with support for MCQ, Answer Writing, and Fill in the Blanks."""
    
    def __init__(self, 
                 config: Optional[MixedConfig] = None,
                 show_answers: bool = False,
                 title: Optional[str] = None,
                 subtitle: Optional[str] = None,
                 exam_title: Optional[str] = None,
                 paper_format: str = 'A4',
                 question_count: int = 0,
                 show_student_info: bool = True):
        """Initialize Mixed Paper Generator with configuration."""
        
        # Create config if not provided
        if not config and (title or subtitle or exam_title):
            config = MixedConfig(
                title=title or 'School Name',
                subtitle=subtitle or 'Class Test',
                exam_title=exam_title or 'Mixed Examination',
                paper_format=paper_format
            )
        
        super().__init__(
            config=config,
            show_answers=show_answers,
            paper_format=paper_format,
            question_count=question_count
        )
        
        self.show_student_info = show_student_info  # Store the parameter

    def write_option(self, label: str, option_text: str, x: float, y: float, 
                    width: float, is_answer: bool = False) -> float:
        """Write a single option and return its height."""
        # Check if we're too close to the footer
        footer_buffer = self.MIN_FOOTER_BUFFER + 2  # Same as MCQPaperGenerator
        if y > (self.h - footer_buffer):
            return 0  # Return 0 instead of -1 to match MCQPaperGenerator
        
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

        # Check if we're too close to the footer
        footer_buffer = self.MIN_FOOTER_BUFFER + 2  # Same as MCQPaperGenerator
        if y > (self.h - footer_buffer):
            return 0  # Return 0 instead of -1 to match MCQPaperGenerator
            
        half_width = (width - self.config.spacing['option_column_gap']) / 2
        label1, text1, is_answer1 = options[start_idx]
        height1 = self.write_option(label1, text1, x, y, half_width, is_answer1)
        
        height2 = 0
        if start_idx + 1 < len(options):
            label2, text2, is_answer2 = options[start_idx + 1]
            x2 = x + half_width + self.config.spacing['option_column_gap']
            height2 = self.write_option(label2, text2, x2, y, half_width, is_answer2)
        
        return max(height1, height2)

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
                "Carefully read all questions before answering.",
                "Answer only on the provided sheet.",
                "Write clearly; follow question format.",
                "Manage your time for all sections."
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
        labels = ['Marks:', 'Duration:']
        values = [f'{self.question_count}', '30min']
        
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
            self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
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

    def _write_mcq_question(self, number: int, question: Dict) -> None:
        """Write a multiple choice question with options."""
        # Calculate total height needed for question and all options
        needed_height = self._measure_mcq_question_height(question['question'], question['choices'])
        
        # Check if the question can fit in a single column
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER
        column_height = effective_page_height - (self.first_page_offset + 5 if self.page_no() == 1 else 20)
        
        # If the question is too tall for a single column, we need to adjust our approach
        if needed_height > column_height:
            # Add a buffer to ensure we don't get too close to the bottom
            buffer = 5
            needed_height = min(needed_height, column_height - buffer)
        
        # Check if current position has enough space and adjust if needed
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # If current position doesn't have enough space, move to next column/page
        if (start_y + needed_height) > effective_page_height:
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_column_space = effective_page_height - right_column_start
                
                if right_column_space >= needed_height:
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
        
        # Update position after adjustment
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
    
        # Store current position in case we need to revert
        original_x = x_start
        original_y = start_y
        original_side = self.current_side
        
        try:
            # Write question number
            question_number_font_size = self.config.font_sizes['question_number']
            question_font_size = self.config.font_sizes['question']
            
            self.set_font('Noto', 'B', question_number_font_size)
            self.set_xy(x_start, start_y)
            self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
            
            # Write question text with vertical alignment
            question_x = x_start + self.config.spacing['question_number_width'] + 1
            self.set_xy(question_x, start_y)
            self.set_font('ArialUni', 'I', question_font_size)
            self.multi_cell(self._question_width, self.config.spacing['line_height'], question['question'])
            
            # Prepare options with answer marking
            options = []
            for idx, choice in enumerate(question['choices']):
                label = f"{chr(65+idx)}."  # A., B., C., D.
                is_answer = (choice == question.get('answer', None))
                options.append((label, choice, is_answer))
            
            # Write options
            options_x = question_x + 2
            current_y = self.get_y() + 1
            
            # Calculate remaining space in current column
            effective_page_height = self.h - self.MIN_FOOTER_BUFFER
            remaining_space = effective_page_height - current_y
            
            # Calculate height needed for options only
            options_height = needed_height - (current_y - start_y)
            
            # If options won't fit in remaining space, move entire question to next column/page
            if options_height > remaining_space:
                # Revert to original position before adjustment
                self.set_xy(original_x, original_y)
                self.current_side = original_side
                
                # Move to next column or page
                if self.current_side == 'left':
                    # Try right column
                    right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    # If we're already on right side, start new page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
                
                # Recursively call _write_mcq_question with the new position
                self._write_mcq_question(number, question)
                return
            
            # Write options with proper layout
            option_idx = 0
            while option_idx < len(options):
                # Check if we can fit two options side by side
                if (option_idx + 1 < len(options) and 
                    self.can_fit_two_options(options[option_idx][1], options[option_idx+1][1])):
                    height = self.write_option_pair(options, option_idx, options_x, current_y, self._options_width)
                    
                    # If options don't fit, move to next column/page
                    if height == 0:  # Changed from -1 to 0 to match MCQPaperGenerator
                        # Revert to original position before adjustment
                        self.set_xy(original_x, original_y)
                        self.current_side = original_side
                        
                        # Move to next column or page
                        if self.current_side == 'left':
                            # Try right column
                            right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                            self.current_side = 'right'
                            self.set_xy(self.w/2 + 2, right_column_start)
                        else:
                            # If we're already on right side, start new page
                            self.add_page()
                            self.current_side = 'left'
                            self.set_xy(10, 20)
                        
                        # Recursively call _write_mcq_question with the new position
                        self._write_mcq_question(number, question)
                        return
                    
                    option_idx += 2
                else:
                    height = self.write_option(
                        options[option_idx][0], 
                        options[option_idx][1], 
                        options_x, 
                        current_y, 
                        self._options_width, 
                        options[option_idx][2]
                    )
                    
                    # If option doesn't fit, move to next column/page
                    if height == 0:  # Changed from -1 to 0 to match MCQPaperGenerator
                        # Revert to original position before adjustment
                        self.set_xy(original_x, original_y)
                        self.current_side = original_side
                        
                        # Move to next column or page
                        if self.current_side == 'left':
                            # Try right column
                            right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                            self.current_side = 'right'
                            self.set_xy(self.w/2 + 2, right_column_start)
                        else:
                            # If we're already on right side, start new page
                            self.add_page()
                            self.current_side = 'left'
                            self.set_xy(10, 20)
                        
                        # Recursively call _write_mcq_question with the new position
                        self._write_mcq_question(number, question)
                        return
                    
                    option_idx += 1
                current_y += height + 1
            
            # Add spacing after question - match MCQPaperGenerator's spacing (1 unit)
            self.set_y(current_y + 1)  # Changed from 2 to 1 to match MCQPaperGenerator
            
        except Exception as e:
            # If anything goes wrong, revert to original position
            self.set_xy(original_x, original_y)
            self.current_side = original_side
            raise e
            
    def _measure_mcq_question_height(self, question_text: str, choices: List[str]) -> float:
        """Calculate the total height needed for an MCQ question with all its options."""
        # Estimate question text height
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        question_height = self.estimate_text_height(question_text, self._question_width)

        # Estimate options height
        total_height = question_height + 1  # Add 1 for spacing after question

        # Calculate actual rendering widths (accounting for label width of 5mm minus 1mm added back = 4mm)
        label_adjustment = 4
        single_option_render_width = self._options_width - label_adjustment

        # For side-by-side: account for gap and label on each side
        half_width_before_label = (self._options_width - self.config.spacing['option_column_gap']) / 2
        half_option_render_width = half_width_before_label - label_adjustment

        i = 0
        while i < len(choices):
            if i + 1 < len(choices) and self.can_fit_two_options(choices[i], choices[i+1]):
                # For side-by-side options, use actual render width
                height = max(
                    self.estimate_text_height(
                        choices[i],
                        half_option_render_width,
                        self.config.font_sizes['option']
                    ),
                    self.estimate_text_height(
                        choices[i+1],
                        half_option_render_width,
                        self.config.font_sizes['option']
                    )
                ) + 0.1  # Minimal padding of 0.1 to match MCQPaperGenerator
                total_height += height
                i += 2
                continue

            # For single options, use actual render width
            option_height = self.estimate_text_height(
                choices[i],
                single_option_render_width,
                self.config.font_sizes['option']
            ) + 0.1  # Minimal padding of 0.1 to match MCQPaperGenerator

            total_height += option_height
            i += 1
            total_height += 0.5  # Add 0.5 between non-side-by-side options to match MCQPaperGenerator

        # Add a very minimal buffer for safety
        buffer_space = 2  # 2 to match MCQPaperGenerator
        return total_height + buffer_space

    def _measure_aw_question_height(self, question: Dict) -> float:
        """Calculate the total height needed for an AW question with potential image."""
        # Estimate question text height
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        question_height = self.estimate_text_height(question['question'], self._question_width)
        
        # Add image height if present
        image_height = 0
        if 'image' in question:
            try:
                # Get image dimensions using PIL directly
                from PIL import Image
                # Check if the path already includes questions_data
                if not question['image'].startswith('questions_data/'):
                    img_path = f"questions_data/{question['image']}"
                with Image.open(img_path) as img:
                    img_w, img_h = img.size
                    img_aspect = img_h / img_w
                    scaled_height = self._question_width * img_aspect
                    image_height = scaled_height + 2  # 2 units padding after image
            except:
                # If image loading fails, continue without the image
                pass
        
        # Add consistent spacing after question
        return question_height + image_height + 2

    def _write_aw_question(self, number: int, question: Dict) -> None:
        """Write an answer writing question with potential image."""
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # Write question number - use config font size
        self.set_font('Noto', 'B', self.config.font_sizes['question_number'])
        self.set_xy(x_start, start_y)
        self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
        
        # Write question text
        question_x = x_start + self.config.spacing['question_number_width'] + 1
        self.set_xy(question_x, start_y)
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        self.multi_cell(self._question_width, self.config.spacing['line_height'], question['question'])
        
        # Add image if present
        if 'image' in question:
            try:
                # Get current Y position after question text
                img_y = self.get_y() + 2  # Add small gap after text
                
                # Place image centered under the question text
                img_path = question['image']
                # Check if the path already includes questions_data
                if not img_path.startswith('questions_data/'):
                    img_path = f"questions_data/{img_path}"
                self.image(img_path, x=question_x, y=img_y, w=self._question_width)
                
                # Update Y position to after the image
                # The error is here - we need to use the image dimensions directly
                # instead of using self.fpdf.get_image_info
                import os
                from PIL import Image
                
                if os.path.exists(img_path):
                    with Image.open(img_path) as img:
                        img_w, img_h = img.size
                        img_aspect = img_h / img_w
                        scaled_height = self._question_width * img_aspect
                        self.set_y(img_y + scaled_height + 2)  # 2 units padding after image
            except Exception as e:
                # If image loading fails, continue without the image
                print(f"Image loading failed: {e}")
                pass
        
        # Add consistent spacing after question/image
        self.set_y(self.get_y() + 2)

    def _measure_fb_question_height(self, question_text: str) -> float:
        """Calculate the total height needed for a Fill in the Blanks question."""
        # Estimate question text height
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        question_height = self.estimate_text_height(question_text, self._question_width)
        
        # Add space for the blank line and spacing after question
        # The blank line needs more space than regular text
        blank_line_height = 6  # Height for the blank line
        spacing_after = 4  # Spacing after the question
        
        return question_height + blank_line_height + spacing_after

    def _write_fb_question(self, number: int, question: Dict) -> None:
        """Write a fill in the blanks question."""
        # First, calculate the height of the question
        question_text = question['question']
        if self.show_answers and 'answer' in question:
            # Replace ___ with answer
            question_text = question_text.replace('___', question['answer'])
            
        question_height = self._measure_fb_question_height(question_text)
        
        # Check if the question can fit in a single column
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER
        column_height = effective_page_height - (self.first_page_offset + 5 if self.page_no() == 1 else 20)
        
        # If the question is too tall for a single column, we need to adjust our approach
        if question_height > column_height:
            # Add a buffer to ensure we don't get too close to the bottom
            buffer = 5
            question_height = min(question_height, column_height - buffer)
        
        # Check if current position has enough space and adjust if needed
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # If current position doesn't have enough space, move to next column/page
        if (start_y + question_height) > effective_page_height:
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_column_space = effective_page_height - right_column_start
                
                if right_column_space >= question_height:
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
        
        # Update position after adjustment
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # Store current position in case we need to revert
        original_x = x_start
        original_y = start_y
        original_side = self.current_side
        
        try:
            # Write question number
            self.set_font('Noto', 'B', self.config.font_sizes['question_number'])
            self.set_xy(x_start, start_y)
            self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
            
            # Write question text
            question_x = x_start + self.config.spacing['question_number_width'] + 1
            self.set_xy(question_x, start_y)
            self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
            
            # Process question text to add underlines for blanks
            question_text = question['question']
            if self.show_answers and 'answer' in question:
                # Replace ___ with answer
                question_text = question_text.replace('___', question['answer'])
            
            # Calculate remaining space in current column
            current_y = self.get_y()
            remaining_space = effective_page_height - current_y
            
            # If question won't fit in remaining space, move entire question to next column/page
            if question_height > remaining_space:
                # Revert to original position before adjustment
                self.set_xy(original_x, original_y)
                self.current_side = original_side
                
                # Move to next column or page
                if self.current_side == 'left':
                    # Try right column
                    right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    # If we're already on right side, start new page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
                
                # Recursively call _write_fb_question with the new position
                self._write_fb_question(number, question)
                return
            
            # Write the question text
            self.multi_cell(self._question_width, self.config.spacing['line_height'], question_text)
            
            # Add consistent spacing after question
            self.set_y(self.get_y() + 2)
            
        except Exception as e:
            # If anything goes wrong, revert to original position
            self.set_xy(original_x, original_y)
            self.current_side = original_side
            raise e

    def _write_mtf_question(self, number: int, question: Dict) -> None:
        """Write a match-the-following question with two columns."""
        # Calculate total height needed for the entire MTF question
        match_pairs = question['match_pairs']
        left_items = {k: v for k, v in match_pairs.items() if not k.isdigit()}
        right_items = {k: v for k, v in match_pairs.items() if k.isdigit()}
        
        # Calculate base height for question text and headers
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        question_height = self.estimate_text_height(question['question'], self._question_width)
        headers_height = 7  # Height for Column A/B headers and spacing
        
        # Calculate height needed for all pairs
        available_width = self._question_width
        col_width = (available_width - 8) / 2  # 8 is spacing between columns
        
        pairs_height = 0
        for left_key in sorted(left_items.keys()):
            # Calculate height for each pair
            left_text = left_items[left_key]
            left_label = f"{left_key}. "
            
            self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
            left_label_width = self.get_string_width(left_label)
            left_content_width = col_width - left_label_width
            
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            left_height = self.estimate_text_height(left_text, left_content_width)
            
            # Get corresponding right item
            right_key = sorted(right_items.keys())[0]  # Just use first one for height estimation
            right_text = right_items[right_key]
            right_label = f"{right_key}. "
            
            self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
            right_label_width = self.get_string_width(right_label)
            right_content_width = col_width - right_label_width
            
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            right_height = self.estimate_text_height(right_text, right_content_width)
            
            # Use maximum height between left and right items
            pair_height = max(left_height, right_height)
            pairs_height += pair_height + 1  # Add 1 point spacing between pairs
        
        # Total height needed
        total_height = question_height + headers_height + pairs_height + 4  # Add 4 points for final spacing
        
        # Check if the question can fit in a single column
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER
        column_height = effective_page_height - (self.first_page_offset + 5 if self.page_no() == 1 else 20)
        
        # If the question is too tall for a single column, we need to adjust our approach
        if total_height > column_height:
            # Add a buffer to ensure we don't get too close to the bottom
            buffer = 5
            total_height = min(total_height, column_height - buffer)
        
        # Check if current position has enough space and adjust if needed
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # If current position doesn't have enough space, move to next column/page
        if (start_y + total_height) > effective_page_height:
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_column_space = effective_page_height - right_column_start
                
                if right_column_space >= total_height:
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
        
        # Update position after adjustment
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # Store current position in case we need to revert
        original_x = x_start
        original_y = start_y
        original_side = self.current_side
        
        try:
            # Write question number and main question text
            self.set_font('Noto', 'B', self.config.font_sizes['question_number'])
            self.set_xy(x_start, start_y)
            self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
            
            question_x = x_start + self.config.spacing['question_number_width'] + 1
            self.set_xy(question_x, start_y)
            self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
            self.multi_cell(self._question_width, self.config.spacing['line_height'], question['question'])
            
            # Calculate remaining space after question text
            current_y = self.get_y()
            remaining_space = effective_page_height - current_y
            
            # If remaining content won't fit, move entire question to next column/page
            if (remaining_space < (headers_height + pairs_height + 4)):
                # Revert to original position before adjustment
                self.set_xy(original_x, original_y)
                self.current_side = original_side
                
                # Move to next column or page
                if self.current_side == 'left':
                    # Try right column
                    right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    # If we're already on right side, start new page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
                
                # Recursively call _write_mtf_question with the new position
                self._write_mtf_question(number, question)
                return
            
            # Move down a bit after the question text
            self.ln(1)
            
            # Calculate column widths and positions
            available_width = self._question_width
            col_width = (available_width - 8) / 2  # 8 is spacing between columns
            
            # Set starting position for columns
            col_start_y = self.get_y()
            left_x = question_x
            right_x = question_x + col_width + 8
            
            # Write column headers
            self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
            self.set_xy(left_x, col_start_y)
            self.cell(col_width, 5, "Column A", 0, 0, 'L')
            self.set_xy(right_x, col_start_y)
            self.cell(col_width, 5, "Column B", 0, 1, 'L')
            self.ln(1)
            
            # Write pairs
            items_start_y = self.get_y()
            current_y = items_start_y
            
            for idx, left_key in enumerate(sorted(left_items.keys())):
                # Write left item
                left_text = left_items[left_key]
                left_label = f"{left_key}. "
                
                self.set_xy(left_x, current_y)
                self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
                left_label_width = self.get_string_width(left_label)
                self.cell(left_label_width, 5, left_label, 0, 0)
                
                self.set_font('ArialUni', '', self.config.font_sizes['option'])
                self.set_xy(left_x + left_label_width, current_y)
                self.multi_cell(col_width - left_label_width, self.config.spacing['line_height'], left_text)
                
                # Get height used by left item
                left_end_y = self.get_y()
                
                # Write right item
                if self.show_answers:
                    # In answer mode, find matching right item
                    answer_map = {v: k for k, v in right_items.items()}
                    right_key = answer_map.get(left_items[left_key], '?')
                else:
                    # In question mode, use corresponding numbered item
                    right_key = sorted(right_items.keys())[idx]
                
                right_text = right_items[right_key]
                right_label = f"{right_key}. "
                
                self.set_xy(right_x, current_y)
                self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
                right_label_width = self.get_string_width(right_label)
                self.cell(right_label_width, 5, right_label, 0, 0)
                
                self.set_font('ArialUni', '', self.config.font_sizes['option'])
                self.set_xy(right_x + right_label_width, current_y)
                self.multi_cell(col_width - right_label_width, self.config.spacing['line_height'], right_text)
                
                # Get height used by right item
                right_end_y = self.get_y()
                
                # Move to next pair position
                current_y = max(left_end_y, right_end_y) + 1
            
            # Add final spacing
            self.set_y(current_y + 2)
            
        except Exception as e:
            # If anything goes wrong, revert to original position
            self.set_xy(original_x, original_y)
            self.current_side = original_side
            raise e

    def check_and_adjust_position(self, needed_height: float, questions: List[Dict], current_idx: int) -> Tuple[bool, int]:
        """Check if there's enough space for content and adjust position if needed."""
        current_y = self.get_y()
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER
        
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
                
                if right_column_space >= needed_height:
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

    def _add_section(self, section: MixedSectionConfig, start_number: int) -> int:
        """Add a section of questions and return the next question number."""
        # Calculate height of first question to prevent orphaned section header
        first_question = section.questions[0]
        
        # Calculate first question height more precisely based on question type
        if section.section_type == 'MCQ':
            # Use the dedicated measurement method for MCQ questions
            first_question_height = self._measure_mcq_question_height(first_question['question'], first_question['choices'])
        elif section.section_type == 'AW':
            # Estimate height for answer writing question
            first_question_height = self._measure_aw_question_height(first_question)
        elif section.section_type == 'FB':
            # Estimate height for fill in the blanks question
            question_text = first_question['question']
            if self.show_answers and 'answer' in first_question:
                # Replace ___ with answer
                question_text = question_text.replace('___', first_question['answer'])
            first_question_height = self._measure_fb_question_height(question_text)
        elif section.section_type == 'MTF':
            # Estimate height for match-the-following question
            match_pairs = first_question['match_pairs']
            left_items = {k: v for k, v in match_pairs.items() if not k.isdigit()}
            
            # Base height for question text
            self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
            question_text_height = self.estimate_text_height(first_question['question'], self._question_width)
            
            # Add height for column headers and spacing
            first_question_height = question_text_height + 15
            
            # Estimate height for each item in the match pairs
            available_width = self._question_width
            col_width = (available_width - 8) / 2  # 8 is spacing between columns
            
            # Estimate height for each pair
            for left_key in sorted(left_items.keys()):
                # Estimate left item height
                left_text = left_items[left_key]
                self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
                left_label = f"{left_key}. "
                left_label_width = self.get_string_width(left_label)
                left_content_width = col_width - left_label_width
                left_height = self.estimate_text_height(left_text, left_content_width, self.config.font_sizes['option'])
                
                # Estimate right item height (using first right item as approximation)
                right_items = {k: v for k, v in match_pairs.items() if k.isdigit()}
                right_key = sorted(right_items.keys())[0]  # Just use the first one for estimation
                right_text = right_items[right_key]
                right_label = f"{right_key}. "
                right_label_width = self.get_string_width(right_label)
                right_content_width = col_width - right_label_width
                right_height = self.estimate_text_height(right_text, right_content_width, self.config.font_sizes['option'])
                
                # Use maximum height between left and right items
                pair_height = max(left_height, right_height)
                first_question_height += pair_height + 1  # Add 1 point spacing between pairs to match MCQs
            
            # Add final spacing after the question
            first_question_height += 2  # Add 2 points spacing after question to match MCQs
        else:
            # Fallback for unknown question types
            first_question_height = 20  # Base height
        
        # Add section header with knowledge of next question's height
        self.add_section(section.name, section.description, first_question_height)
        
        # Write the first question immediately after the section header without position adjustment
        if section.section_type == 'MCQ':
            self._write_mcq_question(start_number, first_question)
        elif section.section_type == 'AW':
            self._write_aw_question(start_number, first_question)
        elif section.section_type == 'FB':
            self._write_fb_question(start_number, first_question)
        elif section.section_type == 'MTF':
            self._write_mtf_question(start_number, first_question)
        
        question_number = start_number + 1
        
        # Write the remaining questions
        for question in section.questions[1:section.required_questions]:
            # Estimate needed height based on question type
            if section.section_type == 'MCQ':
                needed_height = self._measure_mcq_question_height(question['question'], question['choices'])
            elif section.section_type == 'AW':
                # Estimate height for answer writing question
                needed_height = self._measure_aw_question_height(question)
            elif section.section_type == 'FB':
                # Estimate height for fill in the blanks question
                question_text = question['question']
                if self.show_answers and 'answer' in question:
                    # Replace ___ with answer
                    question_text = question_text.replace('___', question['answer'])
                needed_height = self._measure_fb_question_height(question_text)
            elif section.section_type == 'MTF':
                # Estimate height for match-the-following question using the same approach as for the first question
                match_pairs = question['match_pairs']
                left_items = {k: v for k, v in match_pairs.items() if not k.isdigit()}
                
                # Base height for question text
                self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
                question_text_height = self.estimate_text_height(question['question'], self._question_width)
                
                # Add height for column headers and spacing
                needed_height = question_text_height + 15
                
                # Estimate height for each item in the match pairs
                available_width = self._question_width
                col_width = (available_width - 8) / 2  # 8 is spacing between columns
                
                # Estimate height for each pair
                for left_key in sorted(left_items.keys()):
                    # Estimate left item height
                    left_text = left_items[left_key]
                    self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
                    left_label = f"{left_key}. "
                    left_label_width = self.get_string_width(left_label)
                    left_content_width = col_width - left_label_width
                    left_height = self.estimate_text_height(left_text, left_content_width, self.config.font_sizes['option'])
                    
                    # Estimate right item height (using first right item as approximation)
                    right_items = {k: v for k, v in match_pairs.items() if k.isdigit()}
                    right_key = sorted(right_items.keys())[0]  # Just use the first one for estimation
                    right_text = right_items[right_key]
                    right_label = f"{right_key}. "
                    right_label_width = self.get_string_width(right_label)
                    right_content_width = col_width - right_label_width
                    right_height = self.estimate_text_height(right_text, right_content_width, self.config.font_sizes['option'])
                    
                    # Use maximum height between left and right items
                    pair_height = max(left_height, right_height)
                    needed_height += pair_height + 1  # Add 1 point spacing between pairs to match MCQs
                
                # Add final spacing after the question
                needed_height += 2  # Add 2 points spacing after question to match MCQs
            else:
                # Fallback for unknown question types
                needed_height = 20  # Base height
            
            # Check if current position has enough space and adjust if needed
            success, _ = self.check_and_adjust_position(needed_height, [], 0)
            if not success:
                continue
            
            if section.section_type == 'MCQ':
                self._write_mcq_question(question_number, question)
            elif section.section_type == 'AW':
                self._write_aw_question(question_number, question)
            elif section.section_type == 'FB':
                self._write_fb_question(question_number, question)
            elif section.section_type == 'MTF':
                self._write_mtf_question(question_number, question)
            
            question_number += 1
        
        return question_number

    def generate_paper(self, sections: List[MixedSectionConfig]) -> None:
        """Generate the complete mixed question paper from sections."""
        self.add_page()
        question_number = 1
        
        for section in sections:
            question_number = self._add_section(section, question_number)
        
        # Add styled "END" text with gradient-colored asterisks
        self.draw_end_marker()
        
        # Update total question count
        self.question_count = question_number - 1 