try:
    from fpdf import FPDF
except ImportError:
    print("Error importing fpdf. Please make sure it's installed with 'pip install fpdf==1.7.2'")
    raise
import os
from typing import Optional, Dict, Set, List, Tuple
from functools import lru_cache
from .styles import PaperStyles

class PaperConfig:
    """Base configuration class for all paper generators."""
    
    def __init__(self, 
                 title: str = 'Enter School Name (max 60 chars)',
                 subtitle: str = 'Enter Subtitle (max 50 chars)',
                 exam_title: str = 'Enter Exam Title (max 50 chars)',
                 paper_format: str = 'A4',
                 font_paths: Optional[Dict[str, Dict[str, str]]] = None,
                 font_sizes: Optional[Dict[str, int]] = None,
                 spacing: Optional[Dict[str, float]] = None,
                 size_config: str = 'medium'):
        
        # Validate and truncate inputs
        if len(title) > 60:
            raise ValueError("Title must be 60 characters or less")
        if len(subtitle) > 50:
            raise ValueError("Subtitle must be 50 characters or less")
        if len(exam_title) > 50:
            raise ValueError("Exam title must be 50 characters or less")
            
        # Check for placeholder values
        if title == 'Enter School Name (max 60 chars)':
            raise ValueError("Please enter a school name")
        if subtitle == 'Enter Subtitle (max 50 chars)':
            raise ValueError("Please enter a subtitle")
        if exam_title == 'Enter Exam Title (max 50 chars)':
            raise ValueError("Please enter an exam title")
            
        self.title = title
        self.subtitle = subtitle
        self.exam_title = exam_title
        self.paper_format = paper_format
        self.size_config = size_config
        
        # Use centralized styling from PaperStyles
        self.font_paths = font_paths or PaperStyles.FONT_PATHS
        self.font_sizes = font_sizes or PaperStyles.get_font_sizes(size_config)
        self.spacing = spacing or PaperStyles.get_spacing(size_config)

class BasePaperGenerator(FPDF):
    """Base class for all paper generators with common functionality."""
    
    MIN_FOOTER_BUFFER = 12
    
    def __init__(self, 
                 config: Optional[PaperConfig] = None,
                 show_answers: bool = False,
                 paper_format: str = 'A4',
                 question_count: int = 0,
                 strict_ordering: bool = False):
        
        super().__init__(orientation='P', unit='mm', format=paper_format)
        self._initialized_fonts: Set[Tuple[str, str]] = set()
        self.config = config or PaperConfig()
        self.show_answers = show_answers
        self.question_count = question_count
        self.set_name = ""
        self.strict_ordering = strict_ordering
        
        # Initialize common layout settings
        self.set_auto_page_break(auto=True, margin=15)
        self._initialize_fonts()
        
        self.current_side = 'left'
        self.current_column_y = 0
        self.page_start_y = 20
        self.column_height = 0
        self.first_page_offset = 0
        
        # Precompute common measurements
        self._column_width = (self.w/2) - self.config.spacing['column_spacing']
        self._question_width = self._column_width - self.config.spacing['question_number_width'] - 1
        self._options_width = self._column_width - self.config.spacing['question_number_width'] - 3

    def set_set_name(self, name: str) -> None:
        """Set the name of the current set (A, B, C, etc.)."""
        self.set_name = name


    # Class-level font cache to prevent reloading fonts
    _global_font_cache = {}
    
    def _initialize_fonts(self) -> None:
        """Initialize fonts with fallback to standard fonts if custom fonts are not available."""
        for font_family, styles in self.config.font_paths.items():
            for style, path in styles.items():
                font_key = (font_family, style)
                try:
                    if not os.path.exists(path):
                        if font_key not in self._global_font_cache:
                            print(f"Warning: Font file not found: {path}")
                            self._global_font_cache[font_key] = 'fallback'
                        # Use fallback fonts
                        if font_family == 'Stinger':
                            self.set_font('Arial', style)
                        elif font_family == 'Noto':
                            self.set_font('Helvetica', style)
                        elif font_family == 'ArialUni':
                            self.set_font('Arial', style)
                        continue
                        
                    if font_key not in self._initialized_fonts:
                        if font_key not in self._global_font_cache:
                            self.add_font(font_family, style, path, uni=True)
                            self._global_font_cache[font_key] = 'loaded'
                        else:
                            # Font already loaded globally, just add to this instance
                            self.add_font(font_family, style, path, uni=True)
                        self._initialized_fonts.add(font_key)
                except Exception as e:
                    if font_key not in self._global_font_cache:
                        print(f"Warning: Could not load font {font_family} {style}: {e}")
                        self._global_font_cache[font_key] = 'error'
                    # Use fallback fonts
                    if font_family == 'Stinger':
                        self.set_font('Arial', style)
                    elif font_family == 'Noto':
                        self.set_font('Helvetica', style)
                    elif font_family == 'ArialUni':
                        self.set_font('Arial', style)

    def _calculate_optimal_font_size(self, text: str, max_width: float, start_size: int, min_size: int = 16) -> int:
        """Calculate the optimal font size to fit text within a given width."""
        try:
            self.set_font('Stinger', 'B', start_size)
        except RuntimeError:
            self.set_font('Arial', 'B', start_size)
            
        current_size = start_size
        
        while self.get_string_width(text) > max_width and current_size > min_size:
            current_size -= 1
            try:
                self.set_font('Stinger', 'B', current_size)
            except RuntimeError:
                self.set_font('Arial', 'B', current_size)
            
        return current_size

    @lru_cache(maxsize=1024)
    def get_cached_string_width(self, text: str, font_family: str, font_style: str, font_size: int) -> float:
        """Get string width with caching for performance."""
        self.set_font(font_family, font_style, font_size)
        return self.get_string_width(text)

    @lru_cache(maxsize=1024)
    def estimate_text_height(self, text: str, width: float, font_size: int = 12) -> float:
        """Calculate the approximate height needed for text at given width and font size."""
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

    def add_section(self, section_name: str, description: str, next_question_height: float) -> None:
        """Add a new section header with description within the current column."""
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        
        # Get font sizes from configuration
        section_name_font_size = self.config.font_sizes['section_name']
        section_description_font_size = self.config.font_sizes['section_description']
        
        # Calculate needed height for section header more precisely
        self.set_font('Noto', 'B', section_name_font_size)
        section_name_height = self.estimate_text_height(section_name, self._column_width, section_name_font_size)
        
        # Add spacing after section name
        section_name_height += self.config.spacing['section_spacing']['after_section_name']
        
        # Calculate description height
        self.set_font('Noto', 'I', section_description_font_size)
        description_width = self._column_width - self.config.spacing['question_number_width'] - 1
        description_height = self.estimate_text_height(description, description_width, section_description_font_size)
        
        # Add spacing after description
        description_height += self.config.spacing['section_spacing']['after_description']
        
        # Total section header height
        section_height = section_name_height + description_height
        
        # Calculate total needed height including the next question
        total_needed_height = section_height + next_question_height
        
        # Check if current position would orphan the section header
        current_y = self.get_y()
        footer_buffer = self.MIN_FOOTER_BUFFER + 3  # Use class constant with small buffer
        effective_page_height = self.h - footer_buffer
        
        # Add extra spacing if not at top of column
        if current_y > (self.first_page_offset + 5 if self.page_no() == 1 else 20):
            spacing_before = self.config.spacing['section_spacing']['before_section']
            current_y += spacing_before
        
        # Check if there's enough space for both section header and first question
        if (current_y + total_needed_height) > effective_page_height:
            if self.current_side == 'left':
                # Not enough space for section + question, try right column
                self.current_side = 'right'
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                
                if (right_column_start + total_needed_height) > effective_page_height:
                    # Not enough space in right column either, go to next page
                    self.add_page()
                    self.current_side = 'left'
                    self.set_xy(10, 20)
                else:
                    # Move to right column
                    self.set_xy(self.w/2 + 2, right_column_start)
            else:
                # Not enough space in right column, go to next page
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
        else:
            # There is enough space, add spacing if not at top of column
            if current_y > (self.first_page_offset + 5 if self.page_no() == 1 else 20):
                self.ln(self.config.spacing['section_spacing']['before_section'])
        
        x_start = 10 if self.current_side == 'left' else self.w/2 + 2
        current_y = self.get_y()
        
        # Section name in bold and centered
        self.set_font('Noto', 'B', section_name_font_size)
        self.set_xy(x_start, current_y)
        self.multi_cell(self._column_width, self.config.spacing['line_height'], section_name, 0, 'C')
        
        # Space after section name
        self.ln(self.config.spacing['section_spacing']['after_section_name'])
        
        # Section description/instructions in italic and left-aligned
        description_x = x_start + self.config.spacing['question_number_width'] + 1
        description_width = self._column_width - self.config.spacing['question_number_width'] - 1
        
        self.set_font('Noto', 'I', section_description_font_size)
        self.set_xy(description_x, self.get_y())
        self.multi_cell(description_width, self.config.spacing['line_height'], description, 0, 'L')
        
        # Space after description
        self.ln(self.config.spacing['section_spacing']['after_description'])

    def footer(self) -> None:
        """Draw page footer with page number."""
        self.line(10, self.h - 12, self.w - 10, self.h - 12)
        self.set_y(-10)
        self.set_font('Noto', 'I', self.config.font_sizes['footer'])
        self.cell(0, 5, f'Page {self.page_no()}', 0, 0, 'C')

    def measure_option_width(self, option_text: str) -> float:
        """Measure the width of an option including its label."""
        self.set_font('ArialUni', '', self.config.font_sizes['option'])
        return self.get_string_width(f"A. {option_text}")

    def can_fit_two_options(self, option1: str, option2: str) -> bool:
        """Check if two options can fit side by side."""
        width1 = self.measure_option_width(option1)
        width2 = self.measure_option_width(option2)
        total_width = width1 + width2 + self.config.spacing['option_column_gap']
        return total_width <= self._options_width

    def write_option(self, label: str, option_text: str, x: float, y: float, 
                    width: float, is_answer: bool = False) -> float:
        """Write a single option and return its height. Returns -1 if option doesn't fit."""
        # Calculate the height needed for this option
        if is_answer and self.show_answers:
            self.set_font('ArialUni', 'B', self.config.font_sizes['option'])
            option_text_to_measure = option_text + " *"
        else:
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
            option_text_to_measure = option_text
        
        # Estimate the height needed for this option
        option_height = self.estimate_text_height(option_text_to_measure, width - 5 + 1, self.config.font_sizes['option'])
        
        # Check if there's enough space on the current page
        current_y = y
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER
        
        # If option won't fit in remaining space, return -1
        if (current_y + option_height) > effective_page_height:
            return -1
        
        # If we have enough space, write the option
        self.set_xy(x, y)
        label_width = 5
        self.set_font('Noto', 'B', self.config.font_sizes['option_label'])
        self.cell(label_width, 5, label, 0, 0)
        
        self.set_xy(x + label_width, y)
        if is_answer and self.show_answers:
            self.set_font('ArialUni', 'B', self.config.font_sizes['option'])
            option_text = option_text + " *"
        else:
            self.set_font('ArialUni', '', self.config.font_sizes['option'])
        self.multi_cell(width - label_width + 1, 5, option_text, align='L')
        return self.get_y() - y

    def write_option_pair(self, options: List[Tuple[str, str, bool]], start_idx: int, 
                         x: float, y: float, width: float) -> float:
        """Write two options side by side and return the maximum height. Returns -1 if options don't fit."""
        if start_idx >= len(options):
            return 0

        half_width = (width - self.config.spacing['option_column_gap']) / 2
        label1, text1, is_answer1 = options[start_idx]
        height1 = self.write_option(label1, text1, x, y, half_width, is_answer1)
        
        # If first option doesn't fit, return -1
        if height1 == -1:
            return -1
        
        height2 = 0
        if start_idx + 1 < len(options):
            label2, text2, is_answer2 = options[start_idx + 1]
            x2 = x + half_width + self.config.spacing['option_column_gap']
            height2 = self.write_option(label2, text2, x2, y, half_width, is_answer2)
            
            # If second option doesn't fit, return -1
            if height2 == -1:
                return -1
        
        return max(height1, height2)
        
    def draw_end_marker(self) -> None:
        """
        Draw a styled "END" marker with gradient-colored asterisks.
        This is used at the end of question papers to indicate the end of the questions.
        """
        # Check if there's enough space for the end marker in the current column
        y_pos = self.get_y()
        end_marker_height = 20  # Approximate height for the end marker with spacing
        effective_page_height = self.h - self.MIN_FOOTER_BUFFER

        # If there's not enough space in the current column for the end marker
        if (y_pos + end_marker_height) > effective_page_height:
            # Move to the next column or page
            if self.current_side == 'left':
                # Try right column
                right_column_start = self.first_page_offset + 5 if self.page_no() == 1 else 20
                self.current_side = 'right'
                self.set_xy(self.w/2 + 2, right_column_start)
            else:
                # If we're already on right side, create new page
                self.add_page()
                self.current_side = 'left'
                self.set_xy(10, 20)
        
        # Determine which column we're in
        if self.current_side == 'left':
            x = 10
            width = self.w/2 - 12
        else:
            x = self.w/2 + 2
            width = self.w/2 - 12
            
        # Add some space before the END text
        self.ln(10)
        
        # Current y position for the text
        y_pos = self.get_y()
        
        # Center position calculation
        center_x = x + width/2
        
        # Draw the END text with gradient-colored asterisks
        text = "END"
        self.set_font('Noto', 'B', self.config.font_sizes['end_marker'])
        
        # Calculate text width to center properly
        text_width = self.get_string_width(text)
        
        # Draw gradient asterisks (4 on each side)
        asterisk_x_start = center_x - (text_width/2) - 30  # Starting position for asterisks
        
        # Gradient colors from light grey to dark gray (left side)
        left_colors = [
            (200, 200, 200),  # Light grey
            (170, 170, 170),
            (140, 140, 140),
            (110, 110, 110)   # Darker grey
        ]
        
        # Gradient colors from dark gray to light grey (right side)
        right_colors = [
            (110, 110, 110),  # Darker grey
            (140, 140, 140),
            (170, 170, 170),
            (200, 200, 200)   # Light grey
        ]
        
        # Draw left asterisks with gradient
        for i, color in enumerate(left_colors):
            self.set_text_color(color[0], color[1], color[2])
            self.set_xy(asterisk_x_start + (i * 7), y_pos)
            self.cell(7, 5, "*", 0, 0, 'C')
        
        # Draw the END text in black
        self.set_text_color(0, 0, 0)  # Black
        self.set_xy(center_x - text_width/2, y_pos)
        self.cell(text_width, 5, text, 0, 0, 'C')
        
        # Draw right asterisks with gradient
        for i, color in enumerate(right_colors):
            self.set_xy(center_x + text_width/2 + (i * 7), y_pos)
            self.set_text_color(color[0], color[1], color[2])
            self.cell(7, 5, "*", 0, 0, 'C')
        
        # Reset position and text color
        self.ln(10)
        self.set_text_color(0, 0, 0) 