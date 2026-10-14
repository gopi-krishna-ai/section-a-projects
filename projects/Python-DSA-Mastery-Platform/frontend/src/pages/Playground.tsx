import React, { useState } from 'react';
import { api } from '../api/client';
import { 
  PlaySquare, 
  Play, 
  RotateCcw, 
  Clock, 
  Terminal, 
  Sparkles, 
  Code2, 
  Copy, 
  Check 
} from 'lucide-react';

export const Playground: React.FC = () => {
  const defaultSnippet = `# Python Mastery Freeform Scratchpad
# Experiment with advanced Python features, algorithms, or snippets!

def fibonacci_generator(n: int):
    """Generates the first n Fibonacci numbers lazily."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print("First 10 Fibonacci numbers:")
for num in fibonacci_generator(10):
    print(num, end=" ")
print()

# Dictionary comprehension example
squares = {x: x**2 for x in range(1, 6)}
print("Squares dictionary:", squares)
`;

  const [code, setCode] = useState(defaultSnippet);
  const [stdin, setStdin] = useState('');
  const [running, setRunning] = useState(false);
  const [copied, setCopied] = useState(false);
  const [output, setOutput] = useState<{
    stdout: string;
    stderr: string;
    exit_code: number;
    execution_time_ms: number;
    error_type?: string;
  } | null>(null);

  const sampleSnippets = [
    {
      name: 'Custom Context Manager',
      code: `import time
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] Finished in {elapsed * 1000:.3f} ms")

with timer("Sum of 100k items"):
    total = sum(i * 2 for i in range(100_000))
    print(f"Computed sum: {total}")
`
    },
    {
      name: 'Decorator with Arguments',
      code: `import functools

def repeat(num_times: int):
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(num_times):
                print(f"Call #{i + 1}:")
                val = func(*args, **kwargs)
            return val
        return wrapper
    return decorator_repeat

@repeat(num_times=3)
def greet(name: str):
    print(f"Hello, {name}!")

greet("Algorithmic Master")
`
    },
    {
      name: 'Binary Search Implementation',
      code: `def binary_search(arr: list[int], target: int) -> int:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

nums = [1, 3, 5, 7, 9, 11, 13, 15, 17]
target = 11
idx = binary_search(nums, target)
print(f"Target {target} found at index {idx} in {nums}")
`
    }
  ];

  const handleRun = async () => {
    try {
      setRunning(true);
      const res = await api.runCode(code, stdin);
      setOutput(res);
    } catch (err: any) {
      setOutput({
        stdout: '',
        stderr: err.message || 'Execution failed',
        exit_code: 1,
        execution_time_ms: 0,
        error_type: 'RuntimeError'
      });
    } finally {
      setRunning(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Banner */}
      <div className="rounded-2xl p-6 sm:p-8 bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 border border-sky-500/30 flex flex-col md:flex-row md:items-center justify-between gap-6 shadow-xl">
        <div className="max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/20 text-sky-300 text-xs font-bold mb-3 border border-sky-500/30">
            <PlaySquare className="w-3.5 h-3.5" />
            <span>Isolated Python 3.12 Sandboxed Runtime</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight mb-2">
            Coding Playground & Sandbox
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed">
            Run arbitrary Python scripts, test data structure behaviors, inspect outputs, and verify algorithmic hypotheses with zero dependencies or setup required.
          </p>
        </div>

        {/* Quick Samples */}
        <div className="flex flex-wrap md:flex-col gap-2 shrink-0">
          <span className="text-[11px] font-bold text-slate-400 uppercase">Load Templates:</span>
          {sampleSnippets.map((s, idx) => (
            <button
              key={idx}
              onClick={() => {
                setCode(s.code);
                setOutput(null);
              }}
              className="text-left px-3 py-1.5 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-sky-500/50 text-xs text-slate-300 hover:text-white transition-all cursor-pointer truncate max-w-[200px]"
            >
              {s.name}
            </button>
          ))}
        </div>
      </div>

      {/* Editor & Output Panels */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Code Editor */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col">
          <div className="p-4 border-b border-slate-800 bg-slate-950/50 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-sky-400" />
              <span className="text-xs font-bold text-white">main.py</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={handleCopy}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title="Copy code"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
              </button>
              <button
                onClick={() => {
                  setCode(defaultSnippet);
                  setOutput(null);
                }}
                className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                title="Reset code"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
              <button
                disabled={running}
                onClick={handleRun}
                className="px-4 py-1.5 rounded-xl bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white text-xs font-bold transition-all shadow-md shadow-sky-600/30 flex items-center gap-1.5 cursor-pointer"
              >
                <Play className="w-3.5 h-3.5 fill-current" />
                {running ? 'Running...' : 'Run Code'}
              </button>
            </div>
          </div>

          <div className="p-4 bg-slate-950 flex-1 flex flex-col">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              rows={18}
              className="w-full flex-1 font-mono text-xs text-emerald-300 bg-transparent focus:outline-none leading-relaxed resize-y"
              spellCheck={false}
            />
          </div>

          {/* Stdin input tray */}
          <div className="p-3 border-t border-slate-800 bg-slate-950/80">
            <label className="block text-[11px] font-bold text-slate-400 mb-1">
              Standard Input (stdin) - optional:
            </label>
            <input
              type="text"
              placeholder="e.g. 42 or apple banana"
              value={stdin}
              onChange={(e) => setStdin(e.target.value)}
              className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-sky-500"
            />
          </div>
        </div>

        {/* Right: Terminal Output */}
        <div className="bg-slate-900/70 border border-slate-800 rounded-2xl overflow-hidden shadow-lg flex flex-col">
          <div className="p-4 border-b border-slate-800 bg-slate-950/50 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Terminal className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-white">Execution Console</span>
            </div>

            {output && (
              <div className="flex items-center gap-3 text-xs">
                <span className="text-slate-400 flex items-center gap-1">
                  <Clock className="w-3 h-3 text-slate-500" />
                  {output.execution_time_ms} ms
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                  output.exit_code === 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
                }`}>
                  Exit Code: {output.exit_code}
                </span>
              </div>
            )}
          </div>

          <div className="p-4 bg-slate-950 flex-1 font-mono text-xs overflow-y-auto min-h-[350px]">
            {running ? (
              <div className="text-slate-500 animate-pulse">Executing code in subprocess sandbox...</div>
            ) : !output ? (
              <div className="text-slate-600">
                # Click 'Run Code' or press shortcut to execute Python script.
                <br />
                # Output, errors, and execution timings will appear here.
              </div>
            ) : (
              <div className="space-y-3">
                {output.stdout && (
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">
                      Standard Output:
                    </div>
                    <pre className="text-slate-200 whitespace-pre-wrap leading-relaxed">
                      {output.stdout}
                    </pre>
                  </div>
                )}

                {output.stderr && (
                  <div>
                    <div className="text-[10px] font-bold uppercase tracking-wider text-rose-400 mb-1">
                      Standard Error / Traceback:
                    </div>
                    <pre className="text-rose-300 whitespace-pre-wrap leading-relaxed">
                      {output.stderr}
                    </pre>
                  </div>
                )}

                {!output.stdout && !output.stderr && (
                  <div className="text-slate-500">Program executed successfully with no console output.</div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
