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
            'option_label': 9
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
            'option_label': 10
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
            'option_label': 12
        }
    }
    
    # Default font sizes (medium)
    FONT_SIZES = FONT_SIZE_CONFIGS['medium']
    
    # Spacing configurations
    SPACING_CONFIGS = {
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
    
    # Student info section settings
    STUDENT_INFO = {
        'label_font_size': 10,
        'field_spacing': 10,
        'line_offset': 3
    }
    
    # Instructions section settings
    INSTRUCTIONS = {
        'title_font_size': 10,
        'text_font_size': 10,
        'bullet_width': 5,
        'line_spacing': 5,
        'line_height': 5
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