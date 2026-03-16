"""
Code Analysis Module
Analyzes code quality, style, and potential improvements
"""
import ast
from typing import Tuple, List

class CodeAnalyzer:
    def __init__(self):
        self.issues = []
        self.suggestions = []
    
    def analyze(self, code: str, language: str = "python") -> Tuple[List, List, float]:
        """
        Analyze code for issues and improvements
        Returns: (issues, suggestions, quality_score)
        """
        self.issues = []
        self.suggestions = []
        
        if language == "python":
            return self._analyze_python(code)
        else:
            return self._analyze_generic(code)
    
    def _analyze_python(self, code: str) -> Tuple[List, List, float]:
        """Analyze Python code"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            self.issues.append(f"Syntax Error: {str(e)}")
            return self.issues, self.suggestions, 0.0
        
        # Check for code quality issues
        self._check_naming_conventions(tree)
        self._check_documentation(tree)
        self._check_complexity(tree)
        self._check_best_practices(code)
        
        score = self._calculate_score()
        return self.issues, self.suggestions, score
    
    def _analyze_generic(self, code: str) -> Tuple[List, List, float]:
        """Generic code analysis"""
        suggestions = [
            "Add comments to explain complex logic",
            "Use meaningful variable names",
            "Keep functions small and focused",
            "Add error handling",
            "Write unit tests"
        ]
        
        issues = []
        if len(code) < 10:
            issues.append("Code is too short")
        
        return issues, suggestions, 0.5
    
    def _check_naming_conventions(self, tree):
        """Check naming conventions"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('_') and node.name != '__init__':
                    self.suggestions.append(f"Function '{node.name}' should use snake_case")
            elif isinstance(node, ast.ClassDef):
                if not node.name[0].isupper():
                    self.issues.append(f"Class '{node.name}' should use PascalCase")
    
    def _check_documentation(self, tree):
        """Check for docstrings"""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    self.suggestions.append(f"Add docstring to {node.name}")
    
    def _check_complexity(self, tree):
        """Check code complexity"""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = len([n for n in ast.walk(node) if isinstance(n, ast.If)])
                if complexity > 5:
                    self.suggestions.append(f"Function '{node.name}' has high complexity ({complexity} if statements)")
    
    def _check_best_practices(self, code: str):
        """Check for best practices"""
        if "except:" in code:
            self.issues.append("Avoid bare except clauses - specify exception type")
        
        if "import *" in code:
            self.issues.append("Avoid wildcard imports")
        
        if "TODO" in code:
            self.suggestions.append("Resolve TODO comments in code")
    
    def _calculate_score(self) -> float:
        """Calculate overall quality score"""
        score = 1.0
        score -= len(self.issues) * 0.2
        score -= len(self.suggestions) * 0.05
        return max(0.0, min(1.0, score))