import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

function App() {
  const [status, setStatus] = useState("checking...");

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch((err) => setStatus(`error: ${err.message}`));
  }, []);

  return <h1>Backend status: {status}</h1>;
}

export default App;