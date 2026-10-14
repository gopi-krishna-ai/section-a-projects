import React, { useState, useRef } from "react";
import { UploadCloud, FileText, CheckCircle, XCircle, BrainCircuit, RefreshCw, Trophy, ArrowRight, Sparkles } from "lucide-react";
import { useTheme } from "../context/ThemeContext";

type Question = {
  id: number;
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
};

const ADVANCED_QUIZZES: Record<string, Question[]> = {
  general: [
    {
      id: 1,
      question: "Which of the following best describes the principle of 'Polymorphism' in Object-Oriented Programming?",
      options: [
        "The ability of different objects to respond to the same method call in their own way",
        "The process of hiding internal state and requiring all interaction to be performed through an object's methods",
        "The mechanism where a new class inherits properties and behavior from an existing class",
        "The binding of a method call to its implementation at compile time"
      ],
      correctIndex: 0,
      explanation: "Polymorphism allows objects of different classes to be treated as objects of a common superclass. The specific method that gets called is determined dynamically at runtime based on the actual object type."
    },
    {
      id: 2,
      question: "In the context of database transaction concurrency, what phenomenon does the 'Isolation' property of ACID aim to prevent?",
      options: [
        "Data loss during power failures",
        "Dirty reads, non-repeatable reads, and phantom reads",
        "Unauthorized access to sensitive columns",
        "Schema corruption during migrations"
      ],
      correctIndex: 1,
      explanation: "Isolation ensures that concurrent execution of transactions leaves the database in the same state that would have been obtained if the transactions were executed sequentially, preventing phenomena like dirty reads."
    },
    {
      id: 3,
      question: "What is the primary computational advantage of using a Hash Table over a Binary Search Tree for basic key-value lookups?",
      options: [
        "Hash Tables maintain elements in a strictly sorted order",
        "Hash Tables provide O(log n) worst-case time complexity",
        "Hash Tables provide O(1) average time complexity for lookups",
        "Hash Tables use significantly less memory overhead"
      ],
      correctIndex: 2,
      explanation: "While a BST provides O(log n) lookups, a properly sized hash table with a good hash function provides O(1) expected time complexity for lookups, insertions, and deletions."
    },
    {
      id: 4,
      question: "What is the primary difference between a process and a thread in an operating system?",
      options: [
        "Threads run in separate memory spaces, while processes share the same memory space",
        "Processes are lightweight and faster to create than threads",
        "Threads share the same memory space and resources of the process they belong to",
        "A process can only contain a single thread of execution"
      ],
      correctIndex: 2,
      explanation: "A process is an independent execution unit with its own memory space, whereas threads exist within a process and share its memory and resources, making context switching between threads much faster."
    },
    {
      id: 5,
      question: "In the OSI network model, which layer is responsible for logical addressing and routing packets across different networks?",
      options: [
        "Data Link Layer",
        "Network Layer",
        "Transport Layer",
        "Application Layer"
      ],
      correctIndex: 1,
      explanation: "The Network layer (Layer 3) is responsible for routing data packets from a source to a destination across multiple interconnected networks using logical addresses (like IP addresses)."
    }
  ],
  ai: [
    {
      id: 1,
      question: "In the context of neural networks, what is the primary purpose of an activation function?",
      options: [
        "To normalize the input data to a standard range",
        "To introduce non-linearity into the model, allowing it to learn complex patterns",
        "To calculate the gradient of the loss function during backpropagation",
        "To reduce the dimensionality of the feature space"
      ],
      correctIndex: 1,
      explanation: "Without non-linear activation functions (like ReLU, Sigmoid, or Tanh), a deep neural network would simply be a linear regression model, regardless of how many layers it has."
    },
    {
      id: 2,
      question: "Which of the following best describes the 'Vanishing Gradient Problem'?",
      options: [
        "When the learning rate is set too high, causing the model to diverge",
        "When gradients become infinitely large, causing numerical instability",
        "When gradients shrink exponentially as they propagate backward through layers, slowing down early layer training",
        "When the loss function reaches a local minimum instead of a global minimum"
      ],
      correctIndex: 2,
      explanation: "In deep networks (especially those using Sigmoid or Tanh), the chain rule multiplies many small derivatives together, causing the gradient to vanish (approach zero) by the time it reaches early layers."
    },
    {
      id: 3,
      question: "What architectural innovation allows Transformers to effectively handle long-range dependencies in sequences compared to traditional RNNs?",
      options: [
        "Gated Recurrent Units (GRUs)",
        "Self-Attention Mechanism",
        "Convolutional Filters",
        "Stochastic Gradient Descent"
      ],
      correctIndex: 1,
      explanation: "Self-attention allows every token in a sequence to directly attend to every other token, capturing global dependencies in O(1) sequential operations, unlike RNNs which process sequentially."
    },
    {
      id: 4,
      question: "What is the primary purpose of using 'Dropout' during the training of deep neural networks?",
      options: [
        "To increase the learning rate dynamically",
        "To prevent overfitting by randomly disabling a fraction of neurons during each training step",
        "To permanently remove uninformative features from the dataset",
        "To compress the model size for deployment on edge devices"
      ],
      correctIndex: 1,
      explanation: "Dropout acts as a powerful regularization technique. By randomly disabling neurons during training, it forces the network to learn robust, redundant features rather than relying on a small subset of specific neurons."
    },
    {
      id: 5,
      question: "Which algorithm is most fundamentally responsible for updating the weights of a neural network to minimize the loss function?",
      options: [
        "K-Means Clustering",
        "Principal Component Analysis (PCA)",
        "Gradient Descent",
        "Support Vector Machine (SVM)"
      ],
      correctIndex: 2,
      explanation: "Gradient Descent (and its variants like Adam or SGD) iteratively adjusts the network's weights in the opposite direction of the gradient of the loss function with respect to those weights."
    }
  ]
};

export function QuizPage() {
  const { colors } = useTheme();
  
  // State: upload -> analyzing -> quiz -> results
  const [step, setStep] = useState<"upload" | "analyzing" | "quiz" | "results">("upload");
  const [file, setFile] = useState<File | null>(null);
  
  // Quiz State
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const uploadedFile = e.target.files[0];
      setFile(uploadedFile);
      setStep("analyzing");
      
      // Simulate advanced AI analysis
      setTimeout(() => {
        const nameLower = uploadedFile.name.toLowerCase();
        if (nameLower.includes("ai") || nameLower.includes("machine") || nameLower.includes("neural")) {
          setQuestions(ADVANCED_QUIZZES.ai);
        } else {
          setQuestions(ADVANCED_QUIZZES.general);
        }
        setStep("quiz");
        setCurrentIndex(0);
        setSelectedOption(null);
        setIsAnswered(false);
        setScore(0);
      }, 3000);
    }
  };

  const handleOptionSelect = (index: number) => {
    if (isAnswered) return;
    setSelectedOption(index);
    setIsAnswered(true);
    
    if (index === questions[currentIndex].correctIndex) {
      setScore(s => s + 1);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(c => c + 1);
      setSelectedOption(null);
      setIsAnswered(false);
    } else {
      setStep("results");
    }
  };

  const resetQuiz = () => {
    setStep("upload");
    setFile(null);
  };

  const generateMoreQuestions = () => {
    setStep("analyzing");
    setTimeout(() => {
      const nameLower = file?.name.toLowerCase() || "";
      let bank = nameLower.includes("ai") || nameLower.includes("machine") || nameLower.includes("neural") ? ADVANCED_QUIZZES.ai : ADVANCED_QUIZZES.general;
      
      // Shuffle bank to give different questions
      const shuffled = [...bank].sort(() => Math.random() - 0.5);
      
      setQuestions(shuffled);
      setStep("quiz");
      setCurrentIndex(0);
      setSelectedOption(null);
      setIsAnswered(false);
      setScore(0);
    }, 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      <div className="flex items-center gap-3 mb-8">
        <div className="w-12 h-12 rounded-xl flex items-center justify-center shadow-lg" style={{ background: colors.gradient }}>
          <BrainCircuit className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold" style={{ color: colors.text }}>AI Document Quiz</h1>
          <p style={{ color: colors.textLight }}>Upload notes to instantly generate advanced conceptual quizzes.</p>
        </div>
      </div>

      {step === "upload" && (
        <div 
          className="border-2 border-dashed rounded-3xl p-12 text-center transition-all hover:bg-opacity-50 cursor-pointer flex flex-col items-center justify-center"
          style={{ borderColor: colors.primary, background: `${colors.primary}05`, minHeight: "350px" }}
          onClick={() => fileInputRef.current?.click()}
        >
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept=".pdf,.txt,.docx,.md"
            onChange={handleFileUpload} 
          />
          <div className="w-20 h-20 rounded-full flex items-center justify-center mb-6" style={{ background: `${colors.primary}15` }}>
            <UploadCloud className="w-10 h-10" style={{ color: colors.primary }} />
          </div>
          <h3 className="text-xl font-bold mb-2" style={{ color: colors.text }}>Upload Document</h3>
          <p className="mb-6 max-w-md" style={{ color: colors.textLight }}>
            Upload your lecture notes, textbook chapters, or PDFs. Our AI will parse the concepts and generate an advanced multiple-choice assessment.
          </p>
          <button 
            className="px-6 py-3 rounded-xl text-white font-medium flex items-center gap-2 shadow-lg transition-transform hover:scale-105"
            style={{ background: colors.gradient }}
          >
            Select File
          </button>
        </div>
      )}

      {step === "analyzing" && (
        <div className="rounded-3xl p-12 flex flex-col items-center justify-center text-center" style={{ background: colors.cardBg, border: `1px solid ${colors.border}`, minHeight: "350px" }}>
          <div className="relative w-24 h-24 mb-6">
            <div className="absolute inset-0 rounded-full border-4 border-t-transparent animate-spin" style={{ borderColor: `${colors.primary}40`, borderTopColor: colors.primary }}></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <FileText className="w-8 h-8 animate-pulse" style={{ color: colors.primary }} />
            </div>
          </div>
          <h3 className="text-xl font-bold mb-2" style={{ color: colors.text }}>Analyzing Document...</h3>
          <p style={{ color: colors.textLight }}>Extracting key concepts, generating distractors, and formulating advanced questions based on "{file?.name}"</p>
        </div>
      )}

      {step === "quiz" && questions.length > 0 && (
        <div className="rounded-3xl overflow-hidden shadow-sm" style={{ background: colors.cardBg, border: `1px solid ${colors.border}` }}>
          {/* Progress Bar */}
          <div className="h-1.5 w-full bg-black/10">
            <div 
              className="h-full transition-all duration-500 ease-out"
              style={{ width: `${((currentIndex) / questions.length) * 100}%`, background: colors.gradient }}
            ></div>
          </div>
          
          <div className="p-8 md:p-10">
            <div className="flex items-center justify-between mb-8">
              <span className="text-sm font-semibold uppercase tracking-wider" style={{ color: colors.primary }}>
                Question {currentIndex + 1} of {questions.length}
              </span>
              <span className="text-sm font-medium px-3 py-1 rounded-full" style={{ background: `${colors.primary}15`, color: colors.primary }}>
                Score: {score}
              </span>
            </div>

            <h2 className="text-xl md:text-2xl font-bold mb-8 leading-relaxed" style={{ color: colors.text }}>
              {questions[currentIndex].question}
            </h2>

            <div className="space-y-4 mb-8">
              {questions[currentIndex].options.map((opt, i) => {
                const isSelected = selectedOption === i;
                const isCorrect = i === questions[currentIndex].correctIndex;
                
                let btnStyle = { background: colors.bodyBg, borderColor: colors.border, color: colors.text };
                let Icon = null;
                
                if (isAnswered) {
                  if (isCorrect) {
                    btnStyle = { background: "#10b98115", borderColor: "#10b981", color: "#10b981" };
                    Icon = CheckCircle;
                  } else if (isSelected) {
                    btnStyle = { background: "#ef444415", borderColor: "#ef4444", color: "#ef4444" };
                    Icon = XCircle;
                  }
                } else if (isSelected) {
                  btnStyle = { background: `${colors.primary}15`, borderColor: colors.primary, color: colors.text };
                }

                return (
                  <button
                    key={i}
                    onClick={() => handleOptionSelect(i)}
                    disabled={isAnswered}
                    className={`w-full text-left p-5 rounded-2xl border-2 flex items-center justify-between transition-all ${!isAnswered ? 'hover:border-opacity-100 hover:-translate-y-0.5' : ''}`}
                    style={{
                      ...btnStyle,
                      borderOpacity: (!isAnswered && !isSelected) ? 0.5 : 1
                    }}
                  >
                    <span className="font-medium text-[15px] pr-4">{opt}</span>
                    {Icon && <Icon className="w-5 h-5 flex-shrink-0" />}
                  </button>
                );
              })}
            </div>

            {isAnswered && (
              <div className="p-5 rounded-2xl mb-8 animate-fade-in" style={{ background: `${colors.primary}10`, border: `1px solid ${colors.primary}30` }}>
                <h4 className="font-bold flex items-center gap-2 mb-2" style={{ color: colors.primary }}>
                  <BrainCircuit className="w-4 h-4" /> AI Explanation
                </h4>
                <p className="text-sm leading-relaxed" style={{ color: colors.text }}>
                  {questions[currentIndex].explanation}
                </p>
              </div>
            )}

            <div className="flex justify-end">
              <button
                onClick={handleNext}
                disabled={!isAnswered}
                className={`px-8 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all ${isAnswered ? 'shadow-lg' : 'opacity-50 cursor-not-allowed'}`}
                style={{ background: isAnswered ? colors.gradient : colors.border, color: isAnswered ? '#fff' : colors.textLight }}
              >
                {currentIndex < questions.length - 1 ? 'Next Question' : 'View Results'}
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}

      {step === "results" && (
        <div className="rounded-3xl p-12 text-center" style={{ background: colors.cardBg, border: `1px solid ${colors.border}` }}>
          <div className="w-24 h-24 mx-auto rounded-full flex items-center justify-center mb-6 shadow-xl" style={{ background: colors.gradient }}>
            <Trophy className="w-12 h-12 text-white" />
          </div>
          <h2 className="text-3xl font-bold mb-2" style={{ color: colors.text }}>Quiz Completed!</h2>
          <p className="text-lg mb-8" style={{ color: colors.textLight }}>You scored {score} out of {questions.length}</p>
          
          <div className="flex justify-center gap-4">
            <button 
              onClick={generateMoreQuestions}
              className="px-6 py-3 rounded-xl font-medium flex items-center gap-2 transition-all hover:scale-105 shadow-lg"
              style={{ background: colors.gradient, color: '#fff' }}
            >
              <Sparkles className="w-4 h-4" />
              Generate More Questions
            </button>
            <button 
              onClick={resetQuiz}
              className="px-6 py-3 rounded-xl font-medium flex items-center gap-2 transition-all hover:scale-105"
              style={{ background: `${colors.primary}15`, color: colors.primary }}
            >
              <RefreshCw className="w-4 h-4" />
              Upload Another Document
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
