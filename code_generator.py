"""
Code Generation Module
Generates code based on natural language descriptions
"""
from typing import Optional
import re

class CodeGenerator:
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load code templates for different patterns"""
        return {
            "function": """
def {name}({params}):
    """
    {docstring}
    """
    # TODO: Implement function body
    pass
""",
            "class": """
class {name}:
    """
    {docstring}
    """
    
    def __init__(self):
        pass
    
    def method(self):
        pass
""",
            "api_endpoint": """
@app.post("/{endpoint}")
async def {function_name}(request: {model}):
    """
    {docstring}
    """
    try:
        # TODO: Implement logic
        return {{"status": "success"}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
""",
        }
    
    def generate(self, description: str, language: str = "python") -> str:
        """
        Generate code from natural language description
        """
        description_lower = description.lower()
        
        # Detect pattern from description
        if "function" in description_lower or "def " in description_lower:
            return self._generate_function(description, language)
        elif "class" in description_lower:
            return self._generate_class(description, language)
        elif "api" in description_lower or "endpoint" in description_lower:
            return self._generate_api(description, language)
        else:
            return self._generate_generic(description, language)
    
    def _generate_function(self, description: str, language: str) -> str:
        """Generate function code"""
        name = self._extract_name(description, "function")
        params = self._extract_params(description)
        docstring = description
        
        if language == "python":
            return self.templates["function"].format(
                name=name,
                params=params,
                docstring=docstring
            )
        return f"// Function: {{name}}\n// {{docstring}}"
    
    def _generate_class(self, description: str, language: str) -> str:
        """Generate class code"""
        name = self._extract_name(description, "class")
        docstring = description
        
        if language == "python":
            return self.templates["class"].format(
                name=name,
                docstring=docstring
            )
        return f"// Class: {{name}}\n// {{docstring}}"
    
    def _generate_api(self, description: str, language: str) -> str:
        """Generate API endpoint code"""
        endpoint = self._extract_name(description, "endpoint")
        
        if language == "python":
            return self.templates["api_endpoint"].format(
                endpoint=endpoint,
                function_name=f"handle_{{endpoint}}",
                model="Request",
                docstring=description
            )
        return f"// API Endpoint: {{endpoint}}\n// {{description}}"
    
    def _generate_generic(self, description: str, language: str) -> str:
        """Generate generic code snippet"""
        if language == "python":
            return f'"""
{{description}}
"""
# TODO: Implement based on description'
        return f"// {{description}}"
    
    def _extract_name(self, description: str, type_: str) -> str:
        """Extract name from description"""
        words = description.split()
        if type_ in description.lower():
            idx = next((i for i, w in enumerate(words) if type_ in w.lower()), 0)
            if idx + 1 < len(words):
                return words[idx + 1].strip('()[]{}')
        return f"my_{{type_}}"
    
    def _extract_params(self, description: str) -> str:
        """Extract parameters from description"""
        if "parameter" in description.lower() or "param" in description.lower():
            return "self, data"
        return "self"