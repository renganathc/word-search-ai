import { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import { Routes, Route } from "react-router-dom";
import Home from "./Home"
import Download from "./Download"
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

export default function App() {

  return(
    <Routes>
      <Route path="/" element={<Home/>}/>
      <Route path="/download" element={<Download/>}/>
    </Routes>
  )

}
