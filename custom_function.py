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
            },
            "request_to_count": {
                "type": "string",
                "description": "return true if count of a weekday is asked"
            }
        }
     }
     
}]
