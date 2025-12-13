import { useEffect, useState } from "react";
import "./App.css";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

export default function App() {

  useEffect(() => {
    toast.success("The solver currently works only for perfectly aligned grids. Preferably ones downloaded");
  }, []);

  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [solved, setSolved] = useState(false);
  const [wordList, setWordList] = useState("");
  const [loading, setLoading] = useState(false)

  function handleFileChange(e) {
    const file = e.target.files?.[0] ?? null;
    if (!file) return;

    setImageFile(file);

    if (preview) URL.revokeObjectURL(preview);
    const url = URL.createObjectURL(file);
    setPreview(url);
  }

  async function solve() {
    const wl = wordList.trim().replace(/[^A-Za-z,]/g, "").toUpperCase()
    if (!imageFile || !wl) {
      return -1
    }
    setLoading(true)
    try {
      const form_data = new FormData();
      form_data.append("file", imageFile);
      form_data.append("words", wl);
      const res = await fetch("https://word-search-ai-5e2p.onrender.com/solver", {
        method: "POST",
        body: form_data
      })
      console.log(res.status)
      const img_blob = await res.blob();
      console.log(img_blob)
      URL.revokeObjectURL(preview);
      setPreview(URL.createObjectURL(img_blob));
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">

      <h1 className="heading">Word Search AI - Word Puzzle Solver</h1>
      <ToastContainer />

      { !preview ?
      <div className="upload-section">
        <label className="upload-label">
          Upload Image
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
          />
        </label>
      </div>
      : null 
      }

      {preview && (
        <div className="preview-section">
          <img src={preview} className="preview-img" alt="preview" />
        </div>
      )}

      <div className="words-section">
        <label>Words (comma-separated):</label>
        <textarea
          className="words-box"
          placeholder="APPLE, ORANGE, BANANA"
          value={wordList}
          onChange={(e) => setWordList(e.target.value)}
          rows={3}
        />
      </div>

      <button className="solve-btn" onClick={solve} disabled={loading} style={{backgroundColor: loading ? "#2247c1ff" : "#2c5cff"}}>
        {loading ? "Solving…" : "Solve"}
      </button>
    </div>
  );
}
