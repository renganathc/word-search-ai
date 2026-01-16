import { useLocation } from "react-router-dom";
import "./Home.css";
import "react-toastify/dist/ReactToastify.css";

function downloadBlob(url) {
  const a = document.createElement("a");
  a.href = url;
  a.download = "word_search_solved";

  document.body.appendChild(a);
  a.click();
  toast.success("Solved file downloaded");

  document.body.removeChild(a);
}

export default function Download() {

    const { state } = useLocation();
    const image_url = state?.image_url;
    console.log(image_url);

    return (
    <div className="container">

        <h1 className="heading">Word Search AI - Word Puzzle Solver</h1>

        <div className="preview-section">
            <img src={image_url} className="preview-img" alt="preview" />
        </div>

        <button className="solve-btn" onClick={() => downloadBlob(image_url)} style={{backgroundColor: "#c43f1aff", marginTop: 7}}>
            Download
        </button> 

    </div>
  );
}