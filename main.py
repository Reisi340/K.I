"""
AI Code Generator Bot - Main Entry Point
"""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from code_generator import CodeGenerator
from code_analyzer import CodeAnalyzer
from bug_fixer import BugFixer
from test_suite import TestSuite

app = FastAPI(title="AI Code Generator Bot")

# Initialize modules
generator = CodeGenerator()
analyzer = CodeAnalyzer()
fixer = BugFixer()
tester = TestSuite()

# Request/Response Models
class CodeRequest(BaseModel):
    description: str
    language: str = "python"

class CodeResponse(BaseModel):
    code: str
    language: str
    explanation: str

class AnalysisRequest(BaseModel):
    code: str
    language: str = "python"

class AnalysisResponse(BaseModel):
    issues: list
    suggestions: list
    score: float

class BugFixRequest(BaseModel):
    code: str
    language: str = "python"
    error_message: str = None

class BugFixResponse(BaseModel):
    original_code: str
    fixed_code: str
    explanation: str

class TestRequest(BaseModel):
    code: str
    language: str = "python"

class TestResponse(BaseModel):
    test_cases: list
    coverage: float
    results: dict

# Endpoints
@app.get("/")
async def root():
    return {"message": "AI Code Generator Bot v1.0", "status": "active"}

@app.post("/generate", response_model=CodeResponse)
async def generate_code(request: CodeRequest):
    """Generate code from description"""
    try:
        code = generator.generate(request.description, request.language)
        return CodeResponse(
            code=code,
            language=request.language,
            explanation=f"Generated {request.language} code based on: {request.description}"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_code(request: AnalysisRequest):
    """Analyze code for issues and improvements"""
    try:
        issues, suggestions, score = analyzer.analyze(request.code, request.language)
        return AnalysisResponse(
            issues=issues,
            suggestions=suggestions,
            score=score
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/fix-bug", response_model=BugFixResponse)
async def fix_bug(request: BugFixRequest):
    """Fix bugs in code"""
    try:
        fixed_code, explanation = fixer.fix(request.code, request.language, request.error_message)
        return BugFixResponse(
            original_code=request.code,
            fixed_code=fixed_code,
            explanation=explanation
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/test", response_model=TestResponse)
async def generate_tests(request: TestRequest):
    """Generate tests for code"""
    try:
        test_cases, coverage, results = tester.generate_tests(request.code, request.language)
        return TestResponse(
            test_cases=test_cases,
            coverage=coverage,
            results=results
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)