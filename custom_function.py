custom_function = [{
    "name": "run_datagen",
    "description": "Check if the passed string asks for download and running a python file",
    "parameters": {
        "type": "object",
        "properties": {
            "command_to_run": {
                "type": "string",
                "description": "command used for down loading and running the python file"
            },
            "file_url": {
                "type": "string",
                "description": "url of the python file"
            },
            "argument_to_pass": {
                "type": "string",
                "description": "argument or variable passed"
            },
            "is_url_remote": {
                "type": "string",
                "description": "if the url is a web url return true"
            },
            "is_remote_safe": {
                "type": "string",
                "description": "if the url matches `https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py` return true"
            }
        }
    }
}, {
    "name": "run_prettier_format",
    "description": "Check if the passed string asks for formatting a file using prettier",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "path of the file to be formatted"
            },
            "command_to_run": {
                "type": "string",
                "description": "command used for running prettier"
            },
            "is_prettier": {
                "type": "string",
                "description": "check if the command uses prettier"
            },
            "prettier_version": {
                "type": "string",
                "description": "version of prettier being used"
            }
        }
    }
},{
     "name": "run_count_days",
     "description": "Check if the passed string asking to count number of days in a given file",
     "parameters":{
         "type": "object",
        "properties": {
            "input_file_path": {
                "type": "string",
                "description": "path of the file that should be read"
            },
            "weekday_to_count": {
                "type": "string",
                "description": "week day that needs to be counted"
            },
            "output_file_path": {
                "type": "string",
                "description": "path of the file that should be written return"
            }
        }
     }
},{
     "name": "run_sort_array_of_contacts",
     "description": "Check if the passed string asking to sort the array of contacts in a given file and by what attributes",
    "parameters":{
        "type": "object",
        "properties": {
            "input_file_path": {
                "type": "string",
                "description": "path of the input file containing contacts array"
            },
            "output_file_path": {
                "type": "string",
                "description": "path where the sorted contacts should be written"
            },
            "sort_attributes": {
                "type": "array",
                "description": "attributes to sort by in order of priority",
                "items": {
                    "type": "string"
                }
            }
        }
    }
},{
    "name": "run_write_most_recent_logs",
    "description": "Check if the passed string asks to write the most recent log entries from multiple files",
    "parameters": {
        "type": "object",
        "properties": {
            "input_directory": {
                "type": "string",
                "description": "directory path containing the log files"
            },
            "file_pattern": {
                "type": "string",
                "description": "pattern to match log files (*.log)"
            },
            "output_file_path": {
                "type": "string",
                "description": "path where the combined log entries should be written"
            },
            "num_files": {
                "type": "integer",
                "description": "number of most recent log files to process"
            },
            "lines_per_file": {
                "type": "integer",
                "description": "number of lines to extract from each file"
            }
        }
    }
},{
    "name": "run_extract_markdown_titles",
    "description": "Find all Markdown and extract the first occurrance of each H1 tag ",
    "parameters": {
        "type": "object",
        "required": ["input_directory", "output_file_path", "file_pattern"],
        "properties": {
            "input_directory": {
                "type": "string",
                "description": "directory containing markdown files to process"
            },
            "output_file_path": {
                "type": "string",
                "description": "path where the JSON index should be written"
            },
            "file_pattern": {
                "type": "string",
                "description": "pattern to match markdown files (*.md)"
            },
            "tag_pattern": {
                "type": "string",
                "description": "pattern to match H1 tags (# or ===)",
                "default": "#"
            }
        }
    }
},{
    "name": "task_fetch_data_from_api",
    "description": "Check if the passed string asks to fetch data from an API and save it",
    "parameters": {
        "type": "object",
        "properties": {
            "api_url": {
                "type": "string",
                "description": "URL of the API endpoint"
            },
            "http_method": {
                "type": "string", 
                "description": "HTTP method to use (GET, POST, etc.)"
            },
            "output_file_path": {
                "type": "string",
                "description": "path where the API response should be saved"
            },
            "request_headers": {
                "type": "object",
                "description": "headers to include in the API request"
            },
            "request_params": {
                "type": "object",
                "description": "query parameters for the API request"
            }
        }
    }
}, {
    "name": "task_extract_data_from_website",
    "description": "Check if the passed string asks to extract data from a website",
    "parameters": {
        "type": "object",
        "properties": {
            "website_url": {
                "type": "string",
                "description": "URL of the website to scrape"
            },
            "css_selectors": {
                "type": "array",
                "description": "CSS selectors to target specific elements",
                "items": {
                    "type": "string"
                }
            },
            "output_file_path": {
                "type": "string",
                "description": "path where the scraped data should be saved"
            },
            "data_format": {
                "type": "string",
                "description": "format to save the data (json, csv, etc.)"
            },
            "max_depth": {
                "type": "integer",
                "description": "maximum depth of pages to crawl"
            }
        }
    }
}]