import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function askAnalyst() {
    if (!question.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get a response from the analyst.");
      }

      const data = await response.json();
      setAnswer(data.answer);

    } catch (error) {
      console.error(error);
      setAnswer(
        "Sorry, I couldn't analyze your data right now. Please try again."
      );

    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>AI Data Analyst</h1>

      <p>Ask questions about your business data.</p>

      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Example: How did revenue perform on September 20, 2026?"
      />

      <button onClick={askAnalyst} disabled={loading}>
        {loading ? "Analyzing..." : "Ask Analyst"}
      </button>

      {answer && (
        <section>
          <h2>Analyst</h2>
          <ReactMarkdown>{answer}</ReactMarkdown>
        </section>
      )}
    </main>
  );
}

export default App;