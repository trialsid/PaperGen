from typing import List, Dict, Optional, Tuple
from .mcq_generator import MCQPaperGenerator, MCQConfig, SectionConfig
from .styles import PaperStyles

class EnhancedMCQPaperGenerator(MCQPaperGenerator):
    """Enhanced MCQ Paper Generator with MTF (Match the Following) support."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _get_question_text(self, question: Dict, fallback_key: str = 'question') -> List[str]:
        """Extract question_text as array, handling both string and array formats."""
        question_text = question.get('question_text', question.get(fallback_key, ''))
        
        if isinstance(question_text, list):
            return question_text
        elif isinstance(question_text, str):
            return [question_text] if question_text else ['']
        else:
            return ['']
    
    def measure_question_height(self, question_text, choices: List[str], reasoning: Optional[str] = None) -> float:
        """Override to handle question_text arrays."""
        if isinstance(question_text, list):
            # Calculate total height for all question text segments
            total_question_height = 0
            for text in question_text:
                if text.strip():  # Only measure non-empty text
                    text_height = self.estimate_text_height(
                        text, self._question_width, self.config.font_sizes['question']
                    )
                    total_question_height += text_height + 2  # Add spacing between segments
            
            # Call parent method for choices and reasoning calculation
            choices_height = 0
            for choice in choices:
                choice_height = self.estimate_text_height(
                    choice, self._question_width // 2, self.config.font_sizes['option']
                )
                choices_height += choice_height
            
            reasoning_height = 0
            if reasoning and self.show_answers:
                reasoning_height = self.estimate_text_height(
                    reasoning, self._question_width, self.config.font_sizes['option']
                ) + 7
            
            return total_question_height + choices_height + reasoning_height + 5
        else:
            # Fallback to parent method for string input
            return super().measure_question_height(question_text, choices, reasoning)
    
    
    def render_mtf_table(self, left_column: List[str], right_column: List[str], 
                        x: float, y: float, width: float) -> float:
        """Render MTF data as a properly aligned table and return height used."""
        # Calculate column widths
        left_width = width * 0.45  # 45% for left column
        dash_width = width * 0.1   # 10% for dash separator
        right_width = width * 0.45 # 45% for right column
        
        # Set font for table content
        self.set_font('ArialUni', '', self.config.font_sizes['option'])
        
        current_y = y
        max_items = max(len(left_column), len(right_column))
        
        # Render each row
        for i in range(max_items):
            row_height = 0
            
            # Left column item
            if i < len(left_column):
                self.set_xy(x, current_y)
                left_text = left_column[i]
                
                # Calculate height needed for this text
                left_height = self.estimate_text_height(
                    left_text, left_width, self.config.font_sizes['option']
                )
                
                # Write left column text
                self.multi_cell(left_width, self.config.spacing['line_height'], 
                              left_text, align='L')
                row_height = max(row_height, left_height)
            
            # Dash separator
            dash_y = current_y + (row_height / 2) - 2  # Center vertically
            self.set_xy(x + left_width, dash_y)
            self.cell(dash_width, 5, '-', 0, 0, 'C')
            
            # Right column item
            if i < len(right_column):
                self.set_xy(x + left_width + dash_width, current_y)
                right_text = right_column[i]
                
                # Calculate height needed for this text
                right_height = self.estimate_text_height(
                    right_text, right_width, self.config.font_sizes['option']
                )
                
                # Write right column text
                self.multi_cell(right_width, self.config.spacing['line_height'], 
                              right_text, align='L')
                row_height = max(row_height, right_height)
            
            # Move to next row
            current_y += row_height + 1  # Small spacing between rows
        
        return current_y - y
    
    def add_statement_question(self, number: int, question_text: str, statement: str,
                              choices: List[str], correct_answer_index: Optional[int] = None,
                              reasoning: Optional[str] = None) -> None:
        """Add a Statement Based MCQ question."""
        
        # Calculate height needed for the entire question
        needed_height = self.measure_statement_question_height(
            question_text, statement, choices, reasoning
        )
        
        safety_buffer = 5
        total_needed_height = needed_height + safety_buffer
        
        # Check if we need to move to next column/page
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        available_space = effective_page_height - current_y
        
        if total_needed_height > available_space:
            if self.current_side == 'left':
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            return self.add_statement_question(number, question_text, statement, 
                                             choices, correct_answer_index, reasoning)
        
        # Now write the question
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
        
        # Add spacing before statement
        current_y = self.get_y() + 2
        
        # Render statement in a box/highlighted format
        statement_x = question_x + 5
        self.set_xy(statement_x, current_y)
        self.set_font('ArialUni', 'B', self.config.font_sizes['option'])
        self.cell(10, 5, "Statement:", 0, 0)
        
        current_y += 6
        self.set_xy(statement_x, current_y)
        self.set_font('ArialUni', '', self.config.font_sizes['option'])
        self.multi_cell(self._question_width - 5, self.config.spacing['line_height'], statement)
        
        # Add spacing before options
        current_y = self.get_y() + 3
        
        # Write choices using existing logic
        options_x = question_x + 2
        i = 0
        
        while i < len(choices):
            if (i + 1 < len(choices) and 
                self.can_fit_two_options(choices[i], choices[i+1])):
                # Write two options side by side
                half_width = (self._options_width - self.config.spacing['option_column_gap']) / 2
                
                label1 = f"{chr(65+i)}."
                is_answer1 = (i == correct_answer_index)
                option_height1 = self._write_single_option(
                    label1, choices[i], options_x, current_y, half_width, is_answer1
                )
                
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
    
    def add_multiple_statement_question(self, number: int, question_text: str, statements: List[str],
                                      choices: List[str], correct_answer_index: Optional[int] = None,
                                      reasoning: Optional[str] = None) -> None:
        """Add a Multiple Statement MCQ question."""
        
        # Calculate height needed for the entire question
        needed_height = self.measure_multiple_statement_question_height(
            question_text, statements, choices, reasoning
        )
        
        safety_buffer = 5
        total_needed_height = needed_height + safety_buffer
        
        # Check if we need to move to next column/page
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        available_space = effective_page_height - current_y
        
        if total_needed_height > available_space:
            if self.current_side == 'left':
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            return self.add_multiple_statement_question(number, question_text, statements, 
                                                      choices, correct_answer_index, reasoning)
        
        # Now write the question
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
        
        # Add spacing before statements
        current_y = self.get_y() + 2
        
        # Render statements
        statements_x = question_x + 5
        for statement in statements:
            self.set_xy(statements_x, current_y)
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            self.multi_cell(self._question_width - 5, self.config.spacing['line_height'], statement)
            current_y = self.get_y() + 1
        
        # Add spacing before options
        current_y += 2
        
        # Write choices using existing logic
        options_x = question_x + 2
        i = 0
        
        while i < len(choices):
            if (i + 1 < len(choices) and 
                self.can_fit_two_options(choices[i], choices[i+1])):
                # Write two options side by side
                half_width = (self._options_width - self.config.spacing['option_column_gap']) / 2
                
                label1 = f"{chr(65+i)}."
                is_answer1 = (i == correct_answer_index)
                option_height1 = self._write_single_option(
                    label1, choices[i], options_x, current_y, half_width, is_answer1
                )
                
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
    
    def add_sequencing_question(self, number: int, question_text: str, sequence_items: List[str],
                               choices: List[str], correct_answer_index: Optional[int] = None,
                               reasoning: Optional[str] = None) -> None:
        """Add a Sequencing MCQ question."""
        
        # Calculate height needed for the entire question
        needed_height = self.measure_sequencing_question_height(
            question_text, sequence_items, choices, reasoning
        )
        
        safety_buffer = 5
        total_needed_height = needed_height + safety_buffer
        
        # Check if we need to move to next column/page
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        available_space = effective_page_height - current_y
        
        if total_needed_height > available_space:
            if self.current_side == 'left':
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            return self.add_sequencing_question(number, question_text, sequence_items, 
                                              choices, correct_answer_index, reasoning)
        
        # Now write the question
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
        
        # Add spacing before sequence items
        current_y = self.get_y() + 2
        
        # Render sequence items in a box
        items_x = question_x + 5
        for item in sequence_items:
            self.set_xy(items_x, current_y)
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            self.multi_cell(self._question_width - 5, self.config.spacing['line_height'], item)
            current_y = self.get_y() + 1
        
        # Add spacing before options
        current_y += 2
        
        # Write choices using existing logic
        options_x = question_x + 2
        i = 0
        
        while i < len(choices):
            # For sequencing questions, options are usually long, so prefer single column
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
    
    def add_paragraph_question(self, number: int, question_text: str, paragraph: str, question_text_after: str,
                              choices: List[str], correct_answer_index: Optional[int] = None,
                              reasoning: Optional[str] = None) -> None:
        """Add a Paragraph Based MCQ question."""
        
        # Calculate height needed for the entire question
        needed_height = self.measure_paragraph_question_height(
            question_text, paragraph, question_text_after, choices, reasoning
        )
        
        safety_buffer = 5
        total_needed_height = needed_height + safety_buffer
        
        # Check if we need to move to next column/page
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        available_space = effective_page_height - current_y
        
        if total_needed_height > available_space:
            if self.current_side == 'left':
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            return self.add_paragraph_question(number, question_text, paragraph, question_text_after,
                                             choices, correct_answer_index, reasoning)
        
        # Now write the question
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        start_y = self.get_y()
        
        # Write question number and initial text
        self.set_font('Noto', 'B', self.config.font_sizes['question_number'])
        self.set_xy(x_start, start_y)
        self.cell(self.config.spacing['question_number_width'], 5, f"{number}.", 0, 0, 'R')
        
        question_x = x_start + self.config.spacing['question_number_width'] + 1
        self.set_xy(question_x, start_y)
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        self.multi_cell(self._question_width, self.config.spacing['line_height'], question_text)
        
        # Add spacing before paragraph
        current_y = self.get_y() + 2
        
        # Render paragraph in indented format
        paragraph_x = question_x + 5
        self.set_xy(paragraph_x, current_y)
        self.set_font('ArialUni', '', self.config.font_sizes['option'])
        self.multi_cell(self._question_width - 5, self.config.spacing['line_height'], paragraph)
        
        # Add spacing and question text after paragraph
        current_y = self.get_y() + 2
        self.set_xy(question_x, current_y)
        self.set_font('ArialUni', 'I', self.config.font_sizes['question'])
        self.multi_cell(self._question_width, self.config.spacing['line_height'], question_text_after)
        
        # Add spacing before options
        current_y = self.get_y() + 2
        
        # Write choices using existing logic
        options_x = question_x + 2
        i = 0
        
        while i < len(choices):
            if (i + 1 < len(choices) and 
                self.can_fit_two_options(choices[i], choices[i+1])):
                # Write two options side by side
                half_width = (self._options_width - self.config.spacing['option_column_gap']) / 2
                
                label1 = f"{chr(65+i)}."
                is_answer1 = (i == correct_answer_index)
                option_height1 = self._write_single_option(
                    label1, choices[i], options_x, current_y, half_width, is_answer1
                )
                
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
    
    def add_mtf_question(self, number: int, question_text: str, 
                        left_column: List[str], right_column: List[str],
                        choices: List[str], correct_answer_index: Optional[int] = None,
                        reasoning: Optional[str] = None) -> None:
        """Add a Match the Following question with proper table formatting."""
        
        # Calculate height needed for the entire question
        needed_height = self.measure_mtf_question_height(
            question_text, left_column, right_column, choices, reasoning
        )
        
        safety_buffer = 5
        total_needed_height = needed_height + safety_buffer
        
        # Check if we need to move to next column/page
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 5
        effective_page_height = self.h - footer_buffer
        available_space = effective_page_height - current_y
        
        if total_needed_height > available_space:
            if self.current_side == 'left':
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                right_available_space = effective_page_height - right_column_start
                
                if total_needed_height <= right_available_space:
                    self.current_side = 'right'
                    self.set_xy(self.w/2 + 2, right_column_start)
                else:
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
            else:
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
            
            return self.add_mtf_question(number, question_text, left_column, 
                                       right_column, choices, correct_answer_index, reasoning)
        
        # Now write the question
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
        
        # Add some spacing before MTF table
        current_y = self.get_y() + 2
        
        # Render MTF table
        table_width = self._question_width - 5  # Only left indent, no right gap
        table_x = question_x + 5  # Indent the table slightly
        
        mtf_height = self.render_mtf_table(left_column, right_column, 
                                          table_x, current_y, table_width)
        
        # Move to options section
        current_y += mtf_height + 3
        
        # Write choices using existing logic
        options_x = question_x + 2
        i = 0
        
        while i < len(choices):
            if (i + 1 < len(choices) and 
                self.can_fit_two_options(choices[i], choices[i+1])):
                # Write two options side by side
                half_width = (self._options_width - self.config.spacing['option_column_gap']) / 2
                
                label1 = f"{chr(65+i)}."
                is_answer1 = (i == correct_answer_index)
                option_height1 = self._write_single_option(
                    label1, choices[i], options_x, current_y, half_width, is_answer1
                )
                
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
    
    def measure_mtf_question_height(self, question_text: str, left_column: List[str], 
                                   right_column: List[str], choices: List[str], 
                                   reasoning: Optional[str] = None) -> float:
        """Calculate height needed for an MTF question."""
        # Question text height
        question_height = self.estimate_text_height(
            question_text, self._question_width, self.config.font_sizes['question']
        )
        
        total_height = question_height + 2  # Spacing after question
        
        # MTF table height
        max_items = max(len(left_column), len(right_column))
        table_width = self._question_width - 5
        left_width = table_width * 0.45
        right_width = table_width * 0.45
        
        for i in range(max_items):
            row_height = 0
            if i < len(left_column):
                left_height = self.estimate_text_height(
                    left_column[i], left_width, self.config.font_sizes['option']
                )
                row_height = max(row_height, left_height)
            
            if i < len(right_column):
                right_height = self.estimate_text_height(
                    right_column[i], right_width, self.config.font_sizes['option']
                )
                row_height = max(row_height, right_height)
            
            total_height += row_height + 1  # Row height + spacing
        
        total_height += 3  # Spacing after table
        
        # Choices height (reuse existing logic)
        half_options_width = (self._options_width/2) - 1
        i = 0
        while i < len(choices):
            if i + 1 < len(choices) and self.can_fit_two_options(choices[i], choices[i+1]):
                height = max(
                    self.estimate_text_height(
                        f"A. {choices[i]}", half_options_width, self.config.font_sizes['option']
                    ),
                    self.estimate_text_height(
                        f"B. {choices[i+1]}", half_options_width, self.config.font_sizes['option']
                    )
                ) + 0.1
                total_height += height
                i += 2
                continue
            
            option_height = self.estimate_text_height(
                f"A. {choices[i]}", self._options_width, self.config.font_sizes['option']
            ) + 0.1
            total_height += option_height + 0.5
            i += 1
        
        # Reasoning height
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}", self._options_width, self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7
        
        return total_height + 2  # Safety buffer
    
    def measure_statement_question_height(self, question_text: str, statement: str, 
                                        choices: List[str], reasoning: Optional[str] = None) -> float:
        """Calculate height needed for a statement-based question."""
        # Question text height
        question_height = self.estimate_text_height(
            question_text, self._question_width, self.config.font_sizes['question']
        )
        
        # Statement height (with "Statement:" label)
        statement_height = self.estimate_text_height(
            statement, self._question_width - 5, self.config.font_sizes['option']
        ) + 8  # Extra for "Statement:" label
        
        total_height = question_height + statement_height + 5  # Spacing
        
        # Choices height (reuse existing logic)
        total_height += self._calculate_choices_height(choices)
        
        # Reasoning height
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}", self._options_width, self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7
        
        return total_height + 2  # Safety buffer
    
    def measure_multiple_statement_question_height(self, question_text: str, statements: List[str],
                                                 choices: List[str], reasoning: Optional[str] = None) -> float:
        """Calculate height needed for a multiple statement question."""
        # Question text height
        question_height = self.estimate_text_height(
            question_text, self._question_width, self.config.font_sizes['question']
        )
        
        # Statements height
        statements_height = 0
        for statement in statements:
            stmt_height = self.estimate_text_height(
                statement, self._question_width - 5, self.config.font_sizes['option']
            )
            statements_height += stmt_height + 1  # Spacing between statements
        
        total_height = question_height + statements_height + 4  # Spacing
        
        # Choices height
        total_height += self._calculate_choices_height(choices)
        
        # Reasoning height
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}", self._options_width, self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7
        
        return total_height + 2  # Safety buffer
    
    def measure_sequencing_question_height(self, question_text: str, sequence_items: List[str],
                                         choices: List[str], reasoning: Optional[str] = None) -> float:
        """Calculate height needed for a sequencing question."""
        # Question text height
        question_height = self.estimate_text_height(
            question_text, self._question_width, self.config.font_sizes['question']
        )
        
        # Sequence items height
        items_height = 0
        for item in sequence_items:
            item_height = self.estimate_text_height(
                item, self._question_width - 5, self.config.font_sizes['option']
            )
            items_height += item_height + 1  # Spacing between items
        
        total_height = question_height + items_height + 4  # Spacing
        
        # Choices height (prefer single column for sequencing)
        for choice in choices:
            choice_height = self.estimate_text_height(
                f"A. {choice}", self._options_width, self.config.font_sizes['option']
            )
            total_height += choice_height + 1
        
        # Reasoning height
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}", self._options_width, self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7
        
        return total_height + 2  # Safety buffer
    
    def measure_paragraph_question_height(self, question_text: str, paragraph: str, question_text_after: str,
                                        choices: List[str], reasoning: Optional[str] = None) -> float:
        """Calculate height needed for a paragraph-based question."""
        # Initial question text height
        question_height = self.estimate_text_height(
            question_text, self._question_width, self.config.font_sizes['question']
        )
        
        # Paragraph height
        paragraph_height = self.estimate_text_height(
            paragraph, self._question_width - 5, self.config.font_sizes['option']
        )
        
        # Question text after paragraph height
        question_after_height = self.estimate_text_height(
            question_text_after, self._question_width, self.config.font_sizes['question']
        )
        
        total_height = question_height + paragraph_height + question_after_height + 6  # Spacing
        
        # Choices height
        total_height += self._calculate_choices_height(choices)
        
        # Reasoning height
        if reasoning and self.show_answers:
            reasoning_height = self.estimate_text_height(
                f"Explanation: {reasoning}", self._options_width, self.config.font_sizes['option']
            )
            total_height += reasoning_height + 7
        
        return total_height + 2  # Safety buffer
    
    def _calculate_choices_height(self, choices: List[str]) -> float:
        """Helper method to calculate choices height."""
        half_options_width = (self._options_width/2) - 1
        total_height = 0
        i = 0
        while i < len(choices):
            if i + 1 < len(choices) and self.can_fit_two_options(choices[i], choices[i+1]):
                height = max(
                    self.estimate_text_height(
                        f"A. {choices[i]}", half_options_width, self.config.font_sizes['option']
                    ),
                    self.estimate_text_height(
                        f"B. {choices[i+1]}", half_options_width, self.config.font_sizes['option']
                    )
                ) + 0.1
                total_height += height
                i += 2
                continue
            
            option_height = self.estimate_text_height(
                f"A. {choices[i]}", self._options_width, self.config.font_sizes['option']
            ) + 0.1
            total_height += option_height + 0.5
            i += 1
        
        return total_height
    
    def add_question(self, number: int, question_text, choices: List[str], 
                    correct_answer_index: Optional[int] = None, reasoning: Optional[str] = None,
                    question_type: str = "mcq", **kwargs) -> None:
        """Enhanced add_question method that handles all MCQ question types."""
        
        # Convert array to string if needed
        if isinstance(question_text, list):
            # For arrays, render each text segment with appropriate spacing
            combined_text = ""
            for i, text in enumerate(question_text):
                if text.strip():
                    if i > 0:
                        combined_text += " "  # Add space between segments
                    combined_text += text
            question_text = combined_text
        
        if question_type == "mtf-mcq":
            # Handle MTF question
            mtf_data = kwargs.get('mtf_data', {})
            self.add_mtf_question(
                number, question_text, 
                mtf_data.get('left_column', []), 
                mtf_data.get('right_column', []),
                choices, correct_answer_index, reasoning
            )
        elif question_type == "s-mcq":
            # Handle Statement Based MCQ
            statement = kwargs.get('statement', '')
            self.add_statement_question(
                number, question_text, statement,
                choices, correct_answer_index, reasoning
            )
        elif question_type == "ms-mcq":
            # Handle Multiple Statement MCQ
            statements = kwargs.get('statements', [])
            self.add_multiple_statement_question(
                number, question_text, statements,
                choices, correct_answer_index, reasoning
            )
        elif question_type == "seq-mcq":
            # Handle Sequencing MCQ
            sequence_items = kwargs.get('sequence_items', [])
            self.add_sequencing_question(
                number, question_text, sequence_items,
                choices, correct_answer_index, reasoning
            )
        elif question_type == "p-mcq":
            # Handle Paragraph Based MCQ
            paragraph = kwargs.get('paragraph', '')
            question_text_after = kwargs.get('question_text_after', question_text)
            # For p-mcq, the question_text should be empty/generic since the real question comes after paragraph
            intro_text = ""  # No introductory text needed
            self.add_paragraph_question(
                number, intro_text, paragraph, question_text_after,
                choices, correct_answer_index, reasoning
            )
        else:
            # Handle regular MCQ question (default)
            super().add_question(number, question_text, choices, correct_answer_index, reasoning)
    
    def generate_from_sections(self, sections: List[SectionConfig]) -> int:
        """Enhanced generate_from_sections that handles MTF questions."""
        question_number = 1
        total_marks = 0
        
        for section in sections:
            selected_questions = section.questions[:section.required_questions]
            
            questions_with_numbers = []
            for q in selected_questions:
                q_data = q.copy()
                q_data['number'] = question_number
                questions_with_numbers.append(q_data)
                question_number += 1
            
            # Calculate height of first question based on type
            first_question = questions_with_numbers[0]
            q_type = first_question.get('question_type', 'mcq')
            
            if q_type == 'mtf-mcq':
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_mtf_question_height(
                    question_texts,
                    first_question.get('mtf_data', {}).get('left_column', []),
                    first_question.get('mtf_data', {}).get('right_column', []),
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            elif q_type == 's-mcq':
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_statement_question_height(
                    question_texts,
                    first_question.get('statement', ''),
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            elif q_type == 'ms-mcq':
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_multiple_statement_question_height(
                    question_texts,
                    first_question.get('statements', []),
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            elif q_type == 'seq-mcq':
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_sequencing_question_height(
                    question_texts,
                    first_question.get('sequence_items', []),
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            elif q_type == 'p-mcq':
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_paragraph_question_height(
                    question_texts,
                    first_question.get('paragraph', ''),
                    question_texts,
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            else:
                # Default MCQ
                question_texts = self._get_question_text(first_question)
                first_question_height = self.measure_question_height(
                    question_texts,
                    first_question['choices'],
                    first_question.get('reasoning')
                )
            
            # Add section header
            self.add_section(section.name, section.description, first_question_height)
            
            # Add all questions
            for question in questions_with_numbers:
                # Prepare kwargs based on question type
                kwargs = {}
                q_type = question.get('question_type', 'mcq')
                
                if q_type == 'mtf-mcq':
                    kwargs['mtf_data'] = question.get('mtf_data', {})
                elif q_type == 's-mcq':
                    kwargs['statement'] = question.get('statement', '')
                elif q_type == 'ms-mcq':
                    kwargs['statements'] = question.get('statements', [])
                elif q_type == 'seq-mcq':
                    kwargs['sequence_items'] = question.get('sequence_items', [])
                elif q_type == 'p-mcq':
                    kwargs['paragraph'] = question.get('paragraph', '')
                    question_texts = self._get_question_text(question)
                    kwargs['question_text_after'] = question_texts[-1] if question_texts else ''
                
                question_texts = self._get_question_text(question)
                
                self.add_question(
                    question['number'],
                    question_texts,  # Use the helper method result
                    question['choices'],
                    question['choices'].index(question['answer']) if self.show_answers else None,
                    question.get('reasoning') if self.show_answers and 'reasoning' in question else None,
                    q_type,  # Pass question_type as positional parameter
                    **kwargs
                )
                total_marks += section.marks_per_question
        
        self.draw_end_marker()
        
        if hasattr(self, 'question_count'):
            self.question_count = question_number - 1
            
        return total_marks