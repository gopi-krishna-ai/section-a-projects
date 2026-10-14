import sys
import os
import subprocess
import tempfile
import time
import json
from typing import Dict, Any, List, Optional
from backend.config import settings

def get_python_executable() -> str:
    # Prefer py -3.12 on Windows if available, else sys.executable
    if os.name == 'nt':
        return sys.executable
    return "python3"

def execute_python_code(code: str, stdin_input: Optional[str] = None) -> Dict[str, Any]:
    """
    Executes Python code in an isolated subprocess with strict timeout and output limits.
    """
    start_time = time.perf_counter()
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        proc = subprocess.run(
            [get_python_executable(), tmp_path],
            input=stdin_input,
            capture_output=True,
            text=True,
            timeout=settings.EXEC_TIMEOUT_SECONDS,
            encoding="utf-8",
            errors="replace"
        )
        duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        stdout = proc.stdout[:settings.EXEC_MAX_OUTPUT_BYTES]
        stderr = proc.stderr[:settings.EXEC_MAX_OUTPUT_BYTES]

        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": proc.returncode,
            "execution_time_ms": duration_ms,
            "error_type": "Runtime Error" if proc.returncode != 0 else None
        }
    except subprocess.TimeoutExpired:
        duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        return {
            "stdout": "",
            "stderr": f"Time Limit Exceeded: Code execution exceeded {settings.EXEC_TIMEOUT_SECONDS}s timeout limit.",
            "exit_code": -1,
            "execution_time_ms": duration_ms,
            "error_type": "Timeout"
        }
    except Exception as e:
        duration_ms = round((time.perf_counter() - start_time) * 1000.0, 2)
        return {
            "stdout": "",
            "stderr": f"Execution Engine Error: {str(e)}",
            "exit_code": -1,
            "execution_time_ms": duration_ms,
            "error_type": "Engine Failure"
        }
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass

def run_problem_test_cases(user_code: str, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Harness to run user's function against list of test cases in an isolated process.
    Injects a test runner at the bottom of the script that prints a JSON test report.
    """
    harness = f"""
import sys
import json
import time

{user_code}

test_cases = json.loads({json.dumps(json.dumps(test_cases))})
results = []

for idx, tc in enumerate(test_cases):
    tc_input = tc.get("input")
    expected = tc.get("expected_output")
    is_hidden = tc.get("is_hidden", False)
    
    t0 = time.perf_counter()
    passed = False
    actual = None
    err = None
    
    try:
        # Determine callable function or class method
        fn = None
        if "Solution" in globals() and isinstance(globals()["Solution"], type):
            sol_instance = globals()["Solution"]()
            for method_name in dir(sol_instance):
                if not method_name.startswith("_") and callable(getattr(sol_instance, method_name)):
                    fn = getattr(sol_instance, method_name)
                    break
        
        if not fn:
            for candidate in ["two_sum", "twoSum", "max_subarray", "maxSubArray", "longest_substring", "lengthOfLongestSubstring", "coin_change", "coinChange", "solution", "solve"]:
                if candidate in globals() and callable(globals()[candidate]):
                    fn = globals()[candidate]
                    break
        
        if not fn:
            for k, v in list(globals().items()):
                if callable(v) and not isinstance(v, type) and not k.startswith("_") and k not in ["time", "json", "sys", "execute_python_code", "run_problem_test_cases"]:
                    fn = v
                    break
                    
        if not fn:
            raise RuntimeError("No callable solution function found. Please define your function.")
            
        if isinstance(tc_input, dict):
            try:
                actual = fn(**tc_input)
            except TypeError:
                actual = fn(*tc_input.values())
        elif isinstance(tc_input, list):
            actual = fn(*tc_input)
        else:
            actual = fn(tc_input)
            
        # Comparison logic (supports lists, sets, numbers, bools)
        if isinstance(expected, list) and isinstance(actual, (list, tuple)):
            passed = list(actual) == expected or sorted(list(actual)) == sorted(expected)
        else:
            passed = (actual == expected)
            
    except Exception as e:
        err = f"{{type(e).__name__}}: {{str(e)}}"
        passed = False
        
    duration = round((time.perf_counter() - t0) * 1000.0, 2)
    results.append({{
        "test_index": idx + 1,
        "input_str": json.dumps(tc_input) if not is_hidden else "[HIDDEN TEST CASE]",
        "expected_output_str": json.dumps(expected) if not is_hidden else "[HIDDEN]",
        "actual_output_str": json.dumps(actual) if (not is_hidden or not passed) else "[HIDDEN]",
        "passed": bool(passed),
        "is_hidden": bool(is_hidden),
        "execution_time_ms": duration,
        "error": err
    }})

print("__TEST_RESULTS_JSON_START__")
print(json.dumps(results))
print("__TEST_RESULTS_JSON_END__")
"""

    exec_result = execute_python_code(harness)
    if exec_result["error_type"]:
        return {
            "status": exec_result["error_type"],
            "passes_count": 0,
            "total_tests": len(test_cases),
            "execution_time_ms": exec_result["execution_time_ms"],
            "test_results": [],
            "error_output": exec_result["stderr"]
        }

    stdout = exec_result["stdout"]
    start_tag = "__TEST_RESULTS_JSON_START__"
    end_tag = "__TEST_RESULTS_JSON_END__"

    if start_tag in stdout and end_tag in stdout:
        json_part = stdout.split(start_tag)[1].split(end_tag)[0].strip()
        try:
            results_list = json.loads(json_part)
            passes = sum(1 for r in results_list if r.get("passed"))
            total = len(results_list)
            status = "Passed" if passes == total else "Failed"
            return {
                "status": status,
                "passes_count": passes,
                "total_tests": total,
                "execution_time_ms": exec_result["execution_time_ms"],
                "test_results": results_list,
                "error_output": None
            }
        except Exception as e:
            return {
                "status": "Runtime Error",
                "passes_count": 0,
                "total_tests": len(test_cases),
                "execution_time_ms": exec_result["execution_time_ms"],
                "test_results": [],
                "error_output": f"Could not parse test results: {str(e)}\\n{stdout}"
            }
    else:
        return {
            "status": "Runtime Error",
            "passes_count": 0,
            "total_tests": len(test_cases),
            "execution_time_ms": exec_result["execution_time_ms"],
            "test_results": [],
            "error_output": exec_result["stderr"] or stdout
        }
