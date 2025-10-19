class PaperStyles:
    """Centralized styling configuration for all paper generators."""
    
    # Font families and paths
    FONT_PATHS = {
        'Noto': {
            '': './fonts/NotoSans-Regular.ttf',
            'B': './fonts/NotoSans-Bold.ttf',
            'I': './fonts/NotoSans-Italic.ttf'
        },
        'Stinger': {
            'B': './fonts/StingerFitTrial-Bold.ttf'
        },
        'ArialUni': {
            '': './fonts/Arial-Unicode.ttf',
            'I': './fonts/Arial-Unicode-Italic.ttf',
            'B': './fonts/Arial-Unicode-Bold.ttf'
        }
    }
    
    # Font size configurations
    FONT_SIZE_CONFIGS = {
        'x-small': {
            'title': 22,
            'subtitle': 12,
            'exam_title': 16,
            'header': 9,
            'question': 10,
            'option': 10,
            'footer': 7,
            'section_name': 11,
            'section_description': 10,
            'question_number': 8,
            'option_label': 8,
            # Header-specific font sizes
            'set_name': 24,
            'info_table_label': 8,
            'info_table_value': 8,
            'student_info_label': 8,
            'instructions_title': 8,
            'instructions_text': 8,
            # End marker font size
            'end_marker': 12
        },
        'small': {
            'title': 26,
            'subtitle': 14,
            'exam_title': 18,
            'header': 10,
            'question': 11,
            'option': 11,
            'footer': 8,
            'section_name': 13,
            'section_description': 11,
            'question_number': 9,
            'option_label': 9,
            # Header-specific font sizes
            'set_name': 26,
            'info_table_label': 9,
            'info_table_value': 9,
            'student_info_label': 9,
            'instructions_title': 9,
            'instructions_text': 9,
            # End marker font size
            'end_marker': 13
        },
        'medium': {  # Current default
            'title': 30,
            'subtitle': 16,
            'exam_title': 20,
            'header': 12,
            'question': 13,
            'option': 13,
            'footer': 10,
            'section_name': 15,
            'section_description': 13,
            'question_number': 11,
            'option_label': 10,
            # Header-specific font sizes
            'set_name': 28,
            'info_table_label': 10,
            'info_table_value': 10,
            'student_info_label': 10,
            'instructions_title': 10,
            'instructions_text': 10,
            # End marker font size
            'end_marker': 14
        },
        'large': {
            'title': 34,
            'subtitle': 18,
            'exam_title': 22,
            'header': 14,
            'question': 15,
            'option': 15,
            'footer': 12,
            'section_name': 17,
            'section_description': 15,
            'question_number': 13,
            'option_label': 12,
            # Header-specific font sizes
            'set_name': 32,
            'info_table_label': 11,
            'info_table_value': 11,
            'student_info_label': 11,
            'instructions_title': 11,
            'instructions_text': 11,
            # End marker font size
            'end_marker': 16
        }
    }
    
    # Default font sizes (medium)
    FONT_SIZES = FONT_SIZE_CONFIGS['medium']
    
    # Spacing configurations
    SPACING_CONFIGS = {
        'x-small': {
            'question_number_width': 8,
            'option_spacing': 5,
            'footer_height': 10,
            'column_spacing': 12,
            'option_column_gap': 2,
            'line_height': 3.5,
            'section_spacing': {
                'before_section': 3,
                'after_section_name': 1,
                'after_description': 2
            },
            'header_spacing': {
                'after_first_line': 3,           # Gap to student info section
                'after_student_field': 5,        # Gap after roll number
                'instructions_offset': 1,        # Instructions Y offset
                'after_instructions_title': 5,   # Gap after "Instructions:" title
                'between_instructions': 0.5,     # Gap between instruction bullets
                'before_second_line': 1,         # Gap before 2nd horizontal line
                'minimal_gap': 0.5,              # Gap when no student info
                'set_section_height': 8,         # Height of SET section
                'set_vertical_gap': 0.5,         # Vertical gap around SET
                'info_table_row_height': 4,      # Info table row height
                'double_line_gap': 0.5,          # Double line spacing
                'student_field_spacing': 8,      # Spacing between student fields
                'student_line_offset': 2.5       # Offset for underlines in student fields
            },
            'title_block_spacing': {
                'title_line_height': 8,          # Line height for title/school name
                'subtitle_line_height': 7,       # Line height for subtitle
                'exam_title_line_height': 8,     # Line height for exam title
                'after_title_block': 1           # Gap after exam title before first separator
            }
        },
        'small': {
            'question_number_width': 10,
            'option_spacing': 6,
            'footer_height': 12,
            'column_spacing': 15,
            'option_column_gap': 3,
            'line_height': 4,
            'section_spacing': {
                'before_section': 4,
                'after_section_name': 1,
                'after_description': 3
            },
            'header_spacing': {
                'after_first_line': 4,
                'after_student_field': 5.5,      # Gap after roll number (scaled)
                'instructions_offset': 1.5,
                'after_instructions_title': 5.5, # Gap after "Instructions:" title (scaled)
                'between_instructions': 0.75,
                'before_second_line': 1.5,
                'minimal_gap': 0.75,
                'set_section_height': 9,
                'set_vertical_gap': 0.75,
                'info_table_row_height': 4.5,
                'double_line_gap': 0.75,
                'student_field_spacing': 9,
                'student_line_offset': 2.75
            },
            'title_block_spacing': {
                'title_line_height': 9,
                'subtitle_line_height': 8,
                'exam_title_line_height': 9,
                'after_title_block': 1
            }
        },
        'medium': {  # Current default
            'question_number_width': 10,
            'option_spacing': 8,
            'footer_height': 15,
            'column_spacing': 15,
            'option_column_gap': 4,
            'line_height': 5,
            'section_spacing': {
                'before_section': 6,
                'after_section_name': 2,
                'after_description': 4
            },
            'header_spacing': {
                'after_first_line': 5,
                'after_student_field': 6,        # Gap after roll number (scaled)
                'instructions_offset': 2,
                'after_instructions_title': 6,   # Gap after "Instructions:" title (scaled)
                'between_instructions': 1,
                'before_second_line': 2,
                'minimal_gap': 1,
                'set_section_height': 10,
                'set_vertical_gap': 1,
                'info_table_row_height': 5,
                'double_line_gap': 1,
                'student_field_spacing': 10,
                'student_line_offset': 3
            },
            'title_block_spacing': {
                'title_line_height': 10,
                'subtitle_line_height': 9,
                'exam_title_line_height': 10,
                'after_title_block': 1
            }
        },
        'large': {
            'question_number_width': 10,
            'option_spacing': 10,
            'footer_height': 18,
            'column_spacing': 15,
            'option_column_gap': 5,
            'line_height': 6,
            'section_spacing': {
                'before_section': 8,
                'after_section_name': 3,
                'after_description': 5
            },
            'header_spacing': {
                'after_first_line': 6,
                'after_student_field': 7,        # Gap after roll number (scaled)
                'instructions_offset': 2.5,
                'after_instructions_title': 7,   # Gap after "Instructions:" title (scaled)
                'between_instructions': 1.5,
                'before_second_line': 2.5,
                'minimal_gap': 1.25,
                'set_section_height': 11,
                'set_vertical_gap': 1.25,
                'info_table_row_height': 5.5,
                'double_line_gap': 1.25,
                'student_field_spacing': 11,
                'student_line_offset': 3.5
            },
            'title_block_spacing': {
                'title_line_height': 11,
                'subtitle_line_height': 10,
                'exam_title_line_height': 11,
                'after_title_block': 1.5
            }
        }
    }
    
    # Default spacing (medium)
    SPACING = SPACING_CONFIGS['medium']
    
    # Colors (RGB format)
    COLORS = {
        'black': (0, 0, 0),
        'light_grey': (200, 200, 200)
    }
    
    # Header and footer settings
    HEADER_SETTINGS = {
        'first_page_y': 7,
        'subsequent_page_y': 5,
        'line_y_offset': 1
    }

    # Legacy static configs - DEPRECATED
    # These are kept for backwards compatibility but should use size-aware configs instead
    # Use config.font_sizes['student_info_label'] and config.spacing['header_spacing']['student_field_spacing']
    STUDENT_INFO = {
        'label_font_size': 10,  # Use font_sizes['student_info_label'] instead
        'field_spacing': 10,    # Use spacing['header_spacing']['student_field_spacing'] instead
        'line_offset': 3        # Use spacing['header_spacing']['student_line_offset'] instead
    }

    # Legacy static configs - DEPRECATED
    # Use config.font_sizes['instructions_title'], config.font_sizes['instructions_text']
    # and config.spacing['header_spacing'] instead
    INSTRUCTIONS = {
        'title_font_size': 10,  # Use font_sizes['instructions_title'] instead
        'text_font_size': 10,   # Use font_sizes['instructions_text'] instead
        'bullet_width': 5,
        'line_spacing': 5,      # Use spacing['header_spacing']['between_instructions'] instead
        'line_height': 5        # Use spacing['header_spacing']['between_instructions'] instead
    }
    
    @classmethod
    def get_font_sizes(cls, size_config='medium'):
        """Get font sizes for the specified configuration."""
        if size_config not in cls.FONT_SIZE_CONFIGS:
            raise ValueError(f"Invalid font size configuration: {size_config}. "
                            f"Available options: {', '.join(cls.FONT_SIZE_CONFIGS.keys())}")
        return cls.FONT_SIZE_CONFIGS[size_config]
    
    @classmethod
    def get_spacing(cls, size_config='medium'):
        """Get spacing for the specified configuration."""
        if size_config not in cls.SPACING_CONFIGS:
            raise ValueError(f"Invalid spacing configuration: {size_config}. "
                            f"Available options: {', '.join(cls.SPACING_CONFIGS.keys())}")
        return cls.SPACING_CONFIGS[size_config] 