import { useState, useRef } from "react";
import axios from "axios";
import {
  BrainCircuit,
  LayoutDashboard,
  FileText,
  MessageSquare,
  Settings,
  UploadCloud,
  Send,
  Plus,
  Search,
  Menu,
  X,
  Bot,
  User,
  Sparkles,
  Trash2,
  FileUp,
  LoaderCircle,
  CheckCircle2,
  AlertCircle,
  PanelLeftClose,
} from "lucide-react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [documentId, setDocumentId] = useState("");
  const [fileName, setFileName] = useState("");
  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [dragging, setDragging] = useState(false);

  const fileInputRef = useRef(null);
  const chatEndRef = useRef(null);

  const handleUpload = async (file) => {
    if (!file) return;

    const allowed = [".pdf", ".docx", ".txt"];
    const extension = file.name
      .substring(file.name.lastIndexOf("."))
      .toLowerCase();

    if (!allowed.includes(extension)) {
      setError("Only PDF, DOCX and TXT files are supported.");
      return;
    }

    setUploading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(`${API}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setDocumentId(response.data.document_id);
      setFileName(response.data.filename || file.name);
      setMessages([
        {
          role: "assistant",
          content: `Your document "${response.data.filename || file.name}" has been processed successfully. You can now ask questions about it.`,
        },
      ]);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Upload failed. Check whether the backend server is running."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();

    if (!question.trim() || !documentId || asking) return;

    const currentQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      { role: "user", content: currentQuestion },
    ]);

    setQuestion("");
    setAsking(true);
    setError("");

    try {
      const response = await axios.post(`${API}/ask`, {
        document_id: documentId,
        question: currentQuestion,
        top_k: 3,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.answer,
          sources: response.data.sources || [],
        },
      ]);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to generate an answer. Please try again."
      );
    } finally {
      setAsking(false);
      setTimeout(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    }
  };

  const resetDocument = () => {
    setDocumentId("");
    setFileName("");
    setMessages([]);
    setError("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  return (
    <div className="flex min-h-screen bg-[#090e1a] text-slate-200">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-0"
        } fixed inset-y-0 left-0 z-30 flex flex-col overflow-hidden border-r border-white/[0.07] bg-[#0c1322] transition-all duration-300 lg:relative`}
      >
        <div className="flex h-20 items-center gap-3 border-b border-white/[0.07] px-6">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-teal-400/10 text-teal-400">
            <BrainCircuit size={24} />
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white">
              DocuMind<span className="text-teal-400"> AI</span>
            </h1>
            <p className="text-[10px] uppercase tracking-[2px] text-slate-500">
              Intelligent workspace
            </p>
          </div>
        </div>

        <div className="px-4 py-6">
          <p className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[2px] text-slate-500">
            Workspace
          </p>

          <button className="flex w-full items-center gap-3 rounded-xl bg-teal-400/10 px-4 py-3 text-sm font-medium text-teal-300">
            <LayoutDashboard size={18} />
            Dashboard
          </button>

          <button
            onClick={() => fileInputRef.current?.click()}
            className="mt-2 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-400 transition hover:bg-white/[0.05] hover:text-white"
          >
            <FileText size={18} />
            Documents
          </button>

          <button
            onClick={() =>
              document
                .getElementById("chat-section")
                ?.scrollIntoView({ behavior: "smooth" })
            }
            className="mt-2 flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-400 transition hover:bg-white/[0.05] hover:text-white"
          >
            <MessageSquare size={18} />
            AI Assistant
          </button>
        </div>

        <div className="mt-auto border-t border-white/[0.07] p-4">
          <div className="rounded-xl border border-white/[0.07] bg-white/[0.02] p-4">
            <div className="mb-2 flex items-center gap-2 text-teal-400">
              <Sparkles size={16} />
              <span className="text-xs font-semibold">AI Powered</span>
            </div>
            <p className="text-xs leading-5 text-slate-500">
              Ask questions and get answers grounded in your documents.
            </p>
          </div>

          <button className="mt-4 flex w-full items-center gap-3 px-3 py-2 text-sm text-slate-500 hover:text-white">
            <Settings size={17} />
            Settings
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex min-w-0 flex-1 flex-col">
        {/* Header */}
        <header className="flex h-20 items-center justify-between border-b border-white/[0.07] px-5 md:px-8">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="rounded-lg p-2 text-slate-400 hover:bg-white/[0.05]"
            >
              {sidebarOpen ? (
                <PanelLeftClose size={20} />
              ) : (
                <Menu size={20} />
              )}
            </button>
            <div>
              <h2 className="text-sm font-semibold text-white">Dashboard</h2>
              <p className="hidden text-xs text-slate-500 sm:block">
                Your personal document intelligence workspace
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 py-2 sm:flex">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span className="text-xs text-slate-400">Workspace active</span>
            </div>
            <div className="flex h-9 w-9 items-center justify-center rounded-full border border-teal-400/20 bg-teal-400/10 text-sm font-bold text-teal-300">
              U
            </div>
          </div>
        </header>

        {/* Content */}
        <div className="mx-auto w-full max-w-7xl flex-1 space-y-8 p-5 md:p-8">
          {/* Welcome */}
          <section>
            <div className="mb-2 flex items-center gap-2 text-sm text-teal-400">
              <Sparkles size={16} />
              <span>DOCUMENT INTELLIGENCE</span>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white md:text-3xl">
              Turn documents into <span className="text-teal-400">answers.</span>
            </h1>
            <p className="mt-2 text-sm text-slate-400">
              Upload your documents and let AI help you understand them.
            </p>
          </section>

          {/* Stats */}
          <section className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl border border-white/[0.07] bg-[#101827] p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500">Active document</p>
                  <h3 className="mt-2 text-xl font-bold text-white">
                    {documentId ? "1" : "0"}
                  </h3>
                </div>
                <div className="rounded-xl bg-teal-400/10 p-3 text-teal-400">
                  <FileText size={21} />
                </div>
              </div>
              <p className="mt-3 truncate text-xs text-slate-500">
                {fileName || "No document uploaded"}
              </p>
            </div>

            <div className="rounded-2xl border border-white/[0.07] bg-[#101827] p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs text-slate-500">Conversation messages</p>
                  <h3 className="mt-2 text-xl font-bold text-white">
                    {messages.length}
                  </h3>
                </div>
                <div className="rounded-xl bg-indigo-400/10 p-3 text-indigo-300">
                  <MessageSquare size={21} />
                </div>
              </div>
              <p className="mt-3 text-xs text-slate-500">
                Your current session
              </p>
            </div>
          </section>

          {/* Upload */}
          <section>
            <div className="mb-4 flex items-center justify-between">
              <div>
                <h2 className="font-semibold text-white">Upload document</h2>
                <p className="mt-1 text-xs text-slate-500">
                  Add a document to start asking questions.
                </p>
              </div>
              {documentId && (
                <button
                  onClick={resetDocument}
                  className="flex items-center gap-2 text-xs text-red-400 hover:text-red-300"
                >
                  <Trash2 size={14} />
                  Clear session
                </button>
              )}
            </div>

            <div
              onDragOver={(e) => {
                e.preventDefault();
                setDragging(true);
              }}
              onDragLeave={() => setDragging(false)}
              onDrop={(e) => {
                e.preventDefault();
                setDragging(false);
                handleUpload(e.dataTransfer.files?.[0]);
              }}
              onClick={() => !uploading && fileInputRef.current?.click()}
              className={`cursor-pointer rounded-2xl border border-dashed p-8 text-center transition md:p-12 ${
                dragging
                  ? "border-teal-400 bg-teal-400/10"
                  : "border-slate-700 bg-[#101827] hover:border-teal-400/60 hover:bg-[#121e30]"
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                className="hidden"
                onChange={(e) => handleUpload(e.target.files?.[0])}
              />

              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-400/10 text-teal-400">
                {uploading ? (
                  <LoaderCircle className="animate-spin" size={26} />
                ) : (
                  <UploadCloud size={27} />
                )}
              </div>

              <h3 className="font-semibold text-white">
                {uploading
                  ? "Processing your document..."
                  : "Drop your document here"}
              </h3>
              <p className="mt-2 text-sm text-slate-500">
                or{" "}
                <span className="font-medium text-teal-400">
                  browse files
                </span>{" "}
                from your computer
              </p>
              <p className="mt-4 text-[11px] text-slate-600">
                Supported formats: PDF, DOCX, TXT
              </p>
            </div>

            {documentId && (
              <div className="mt-3 flex items-center gap-3 rounded-xl border border-emerald-400/20 bg-emerald-400/[0.06] p-4">
                <CheckCircle2 className="shrink-0 text-emerald-400" size={19} />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-emerald-300">
                    {fileName}
                  </p>
                  <p className="text-xs text-slate-500">
                    Document processed and ready for questions
                  </p>
                </div>
              </div>
            )}
          </section>

          {/* Chat */}
          <section id="chat-section">
            <div className="mb-4">
              <h2 className="font-semibold text-white">Ask your documents</h2>
              <p className="mt-1 text-xs text-slate-500">
                Get contextual answers using retrieval-augmented generation.
              </p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-white/[0.07] bg-[#101827]">
              <div className="flex items-center justify-between border-b border-white/[0.07] px-5 py-4">
                <div className="flex items-center gap-3">
                  <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-teal-400/10 text-teal-400">
                    <Bot size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-white">
                      DocuMind Assistant
                    </p>
                    <p className="text-[11px] text-slate-500">
                      {documentId ? "Document connected" : "Waiting for document"}
                    </p>
                  </div>
                </div>
                <span className="rounded-full bg-teal-400/10 px-3 py-1 text-[10px] font-medium text-teal-300">
                  RAG Assistant
                </span>
              </div>

              <div className="flex min-h-[300px] flex-col gap-5 p-5 md:min-h-[380px]">
                {messages.length === 0 ? (
                  <div className="m-auto max-w-sm py-8 text-center">
                    <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-teal-400/10 text-teal-400">
                      <MessageSquare size={25} />
                    </div>
                    <h3 className="font-semibold text-white">
                      Start a conversation
                    </h3>
                    <p className="mt-2 text-sm leading-6 text-slate-500">
                      Upload a document first. Then ask anything about its
                      contents.
                    </p>
                  </div>
                ) : (
                  messages.map((message, index) => (
                    <div
                      key={index}
                      className={`flex gap-3 ${
                        message.role === "user" ? "flex-row-reverse" : ""
                      }`}
                    >
                      <div
                        className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
                          message.role === "user"
                            ? "bg-indigo-400/10 text-indigo-300"
                            : "bg-teal-400/10 text-teal-400"
                        }`}
                      >
                        {message.role === "user" ? (
                          <User size={17} />
                        ) : (
                          <Bot size={17} />
                        )}
                      </div>

                      <div
                        className={`max-w-[85%] rounded-2xl px-4 py-3 text-sm leading-7 ${
                          message.role === "user"
                            ? "bg-teal-400/10 text-teal-100"
                            : "border border-white/[0.06] bg-[#151f30] text-slate-300"
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{message.content}</p>

                        {message.sources?.length > 0 && (
                          <div className="mt-4 border-t border-white/[0.08] pt-3">
                            <p className="mb-2 text-[10px] font-semibold uppercase tracking-wider text-teal-400">
                              Sources
                            </p>
                            {message.sources.map((source, sourceIndex) => (
                              <div
                                key={sourceIndex}
                                className="mb-2 rounded-lg bg-black/20 p-3 text-xs text-slate-400"
                              >
                                <p className="mb-1 font-medium text-slate-300">
                                  Source {sourceIndex + 1}
                                </p>
                                <p className="line-clamp-3">
                                  {source.text || source.content || "Retrieved document context"}
                                </p>
                                {source.score !== undefined && (
                                  <p className="mt-1 text-teal-400">
                                    Similarity: {Number(source.score).toFixed(3)}
                                  </p>
                                )}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                )}

                {asking && (
                  <div className="flex items-center gap-3 text-sm text-slate-400">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-teal-400/10 text-teal-400">
                      <Bot size={17} />
                    </div>
                    <span className="flex items-center gap-2">
                      Thinking
                      <LoaderCircle className="animate-spin" size={14} />
                    </span>
                  </div>
                )}

                <div ref={chatEndRef} />
              </div>

              {error && (
                <div className="mx-5 mb-3 flex items-start gap-2 rounded-xl border border-red-400/20 bg-red-400/[0.06] p-3 text-xs text-red-300">
                  <AlertCircle className="mt-0.5 shrink-0" size={15} />
                  {error}
                </div>
              )}

              <form
                onSubmit={handleSend}
                className="border-t border-white/[0.07] p-4"
              >
                <div className="flex items-center gap-3 rounded-xl border border-white/[0.08] bg-[#0b1220] px-4 py-2 focus-within:border-teal-400/50">
                  <input
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    disabled={!documentId || asking}
                    placeholder={
                      documentId
                        ? "Ask something about your document..."
                        : "Upload a document to start chatting..."
                    }
                    className="min-w-0 flex-1 bg-transparent py-2 text-sm text-white outline-none placeholder:text-slate-600 disabled:cursor-not-allowed"
                  />
                  <button
                    type="submit"
                    disabled={!documentId || !question.trim() || asking}
                    className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-teal-400 text-[#07131a] transition hover:bg-teal-300 disabled:cursor-not-allowed disabled:opacity-30"
                  >
                    <Send size={16} />
                  </button>
                </div>
                <p className="mt-2 text-center text-[10px] text-slate-600">
                  AI-generated responses can contain mistakes. Verify
                  important information with the original document.
                </p>
              </form>
            </div>
          </section>
        </div>

        <footer className="border-t border-white/[0.06] px-8 py-5 text-center text-[11px] text-slate-600">
          DocuMind AI · Intelligent Document Assistant
        </footer>
      </main>
    </div>
  );
}