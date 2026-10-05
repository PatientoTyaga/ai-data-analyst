import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

type UploadResult = {
  dataset_id: string;
  filename: string;
  columns: string[];
  sample_rows: Record<string, string>[];
};

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [step, setStep] = useState<"upload" | "mapping" | "analyst">("upload");
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [uploadResult, setUploadResult] = useState<UploadResult | null>(null);
  const [statusValues, setStatusValues] = useState<string[]>([]);
  const [mapping, setMapping] = useState({
    transaction_date: "",
    revenue: "",
    region: "",
    status: "",
    valid_status: "",
    cancelled_status: "",
  });

  const mappingComplete =
    mapping.transaction_date &&
    mapping.revenue &&
    mapping.region &&
    mapping.status &&
    mapping.valid_status &&
    mapping.cancelled_status;

  async function loadStatusValues(column: string) {
    if (!uploadResult || !column) {
      setStatusValues([]);
      return;
    }

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/column-values",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            dataset_id: uploadResult.dataset_id,
            column: column,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Unable to load status values.");
      }

      const data = await response.json();

      setStatusValues(data.values);

    } catch (error) {
      console.error(error);
      setStatusValues([]);
    }
  }

  async function confirmMapping() {
    if (!uploadResult || !mappingComplete) {
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/mapping", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          dataset_id: uploadResult.dataset_id,
          original_filename: uploadResult.filename,
          ...mapping,
        }),
      });

      if (!response.ok) {
        throw new Error("Unable to save mapping.");
      }

      const data = await response.json();

      console.log("Confirmed mapping:", data);

      setStep("analyst");

    } catch (error) {
      console.error(error);
    }
  }

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
          dataset_id: uploadResult?.dataset_id,
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

  async function uploadData() {
    if (!uploadedFile) {
      return;
    }

    setUploading(true);
    setUploadError("");

    try {
      const formData = new FormData();
      formData.append("file", uploadedFile);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed.");
      }

      const data = await response.json();
      setUploadResult(data);

      console.log("Uploaded data:", data);

      setStep("mapping");

    } catch (error) {
      console.error(error);
      setUploadError("Unable to upload the file. Please try again.");

    } finally {
      setUploading(false);
    }
  }

  if (step === "upload") {
    return (
      <main>
        <h1>AI Data Analyst</h1>
        <p>Upload your business data to begin.</p>

        <section>
          <h2>Upload Data</h2>

          <input
            type="file"
            accept=".csv"
            onChange={(event) => {
              const file = event.target.files?.[0];

              if (file) {
                setUploadedFile(file);
              }
            }}
          />

          <button
            onClick={uploadData}
            disabled={!uploadedFile || uploading}
          >
            {uploading ? "Uploading..." : "Continue"}
          </button>

          {uploadError && <p>{uploadError}</p>}
        </section>
      </main>
    );
  }

  if (step === "mapping" && uploadResult) {
    const columnMappings = [
      ["transaction_date", "Transaction Date"],
      ["revenue", "Revenue"],
      ["region", "Region"],
      ["status", "Status"],
    ] as const;

    return (
      <main>
        <h1>Review Data Mapping</h1>

        <p>
          Tell us what each column in {uploadResult.filename} represents.
        </p>

        <section>
          {columnMappings.map(([key, label]) => (
            <div className="mapping-field" key={key}>
              <label htmlFor={key}>{label}</label>

              <select
                id={key}
                value={mapping[key]}
                onChange={(event) => {
                  const value = event.target.value;

                  setMapping({
                    ...mapping,
                    [key]: value,
                    ...(key === "status"
                      ? {
                          valid_status: "",
                          cancelled_status: "",
                        }
                      : {}),
                  });

                  if (key === "status") {
                    loadStatusValues(value);
                  }
                }}
              >
                <option value="">Select column</option>

                {uploadResult.columns.map((column) => (
                  <option key={column} value={column}>
                    {column}
                  </option>
                ))}
              </select>
            </div>
          ))}

          <div className="mapping-field">
            <label htmlFor="valid_status">Successful Status</label>

            <select
              id="valid_status"
              value={mapping.valid_status}
              disabled={!mapping.status}
              onChange={(event) =>
                setMapping({
                  ...mapping,
                  valid_status: event.target.value,
                })
              }
            >
              <option value="">Select value</option>

              {statusValues.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>

          <div className="mapping-field">
            <label htmlFor="cancelled_status">Cancelled Status</label>

            <select
              id="cancelled_status"
              value={mapping.cancelled_status}
              disabled={!mapping.status}
              onChange={(event) =>
                setMapping({
                  ...mapping,
                  cancelled_status: event.target.value,
                })
              }
            >
              <option value="">Select value</option>

              {statusValues.map((value) => (
                <option key={value} value={value}>
                  {value}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={confirmMapping}
            disabled={!mappingComplete}
          >
            Confirm Mapping
          </button>
        </section>
      </main>
    );
  }

  function startOver() {
    setUploadedFile(null);
    setUploadResult(null);
    setStatusValues([]);

    setMapping({
      transaction_date: "",
      revenue: "",
      region: "",
      status: "",
      valid_status: "",
      cancelled_status: "",
    });

    setQuestion("");
    setAnswer("");
    setUploadError("");
    setStep("upload");
  }

  return (
    <main>
      <h1>AI Data Analyst</h1>

      <p>Ask questions about your business data.</p>

      {uploadResult && (
        <p className="dataset-label">
          Analyzing: <strong>{uploadResult.filename}</strong>
        </p>
      )}

      <textarea
        value={question}
        onChange={(event) => setQuestion(event.target.value)}
        placeholder="Example: How did revenue perform on September 20, 2026?"
      />

      <div className="analyst-actions">
        <button onClick={askAnalyst} disabled={loading}>
          {loading ? "Analyzing..." : "Ask Analyst"}
        </button>

        <button
          type="button"
          className="secondary-button"
          onClick={startOver}
        >
          Analyze Another Dataset
        </button>
      </div>

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