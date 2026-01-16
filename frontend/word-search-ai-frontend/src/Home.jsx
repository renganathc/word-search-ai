import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./Home.css";
import { Link, useNavigate } from "react-router-dom";
import "react-toastify/dist/ReactToastify.css";

export default function Home() {

  useEffect(() => {
    toast.success("The solver currently works only for perfectly aligned grids. Preferably ones downloaded");
  }, []);

  const [imageFile, setImageFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [solverType, setSolverType] = useState("auto");
  const [wordList, setWordList] = useState("");
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate();

  function handleFileChange(e) {
    const file = e.target.files?.[0] ?? null;
    if (!file) return;

    setImageFile(file);

    if (preview) URL.revokeObjectURL(preview);
    const url = URL.createObjectURL(file);
    setPreview(url);
  }

  async function solve(solver_type) {
    const wl = wordList.trim().replace(/[^A-Za-z,]/g, "").toUpperCase()
    if (!imageFile || (!wl && solver_type == "manual")) {
      return -1
    }
    setLoading(true)
    setPreview("/solving.gif")
    try {
      const form_data = new FormData();
      form_data.append("file", imageFile);
      form_data.append("words", wl);
      form_data.append("solver_type", solver_type);
      // const solver_backend = "http://localhost:7860/solver";
      // const solver_backend = "https://word-search-ai-5e2p.onrender.com/solver";
      const solver_backend = "https://renganathc-word-search-ai.hf.space/solver";
      const res = await fetch(solver_backend, {
        method: "POST",
        body: form_data
      });
      console.log(res.status);
      const img_blob = await res.blob();
      //console.log(img_blob)
      //URL.revokeObjectURL(preview);
      //setPreview(URL.createObjectURL(img_blob));
      navigate("/download", {state: {image_url: URL.createObjectURL(img_blob)}});
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

      {solverType == "manual" ? (
        <>
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
          <button className="solve-btn" onClick={() => {solve("manual")}} disabled={loading} style={{backgroundColor: loading ? "#2247c1ff" : "#2c5cff"}}>
            {loading ? "Solving…" : "Solve"}
          </button> 
        </>
      ) : (
        <>
          <button className="auto-solve-btn" onClick={() => {solve("auto")}} disabled={loading} style={{backgroundColor: loading ? "#2247c1ff" : "#2c5cff"}}>
            {loading ? "Solving…" : "Auto Solve"}
          </button> 
          {!loading ? (
            <>
                <p style={{margin: 0, padding: 0}}>- or -</p>
                <button className="manual-solve-btn" onClick={() => {setSolverType("manual")}} disabled={loading}>
                    Enter Words Manually
                </button>
            </>
          ) : <></>}
        </>
      )}

    </div>
  );
}
