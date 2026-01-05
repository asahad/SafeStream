import { useState, useEffect } from "react";
import { analyzeVideo, livePoll } from "./api/client";

export default function App() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [live, setLive] = useState(false);

  useEffect(() => {
    if (!live) return;
    const id = setInterval(async () => {
      const res = await livePoll(url);
      setData(res);
    }, 20000);
    return () => clearInterval(id);
  }, [live, url]);

  return (
    <div style={{ maxWidth: 900, margin: "auto", padding: 20 }}>
      <h1>SafeStream</h1>
      <input
        placeholder="Paste YouTube URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "100%", padding: 10 }}
      />
      <button onClick={async () => setData(await analyzeVideo(url))}>
        Analyze
      </button>
      <button onClick={() => setLive(!live)}>
        {live ? "Stop Live" : "Start Live"}
      </button>

      {data && (
        <>
          <h3>Moderation Summary</h3>
          <pre>{data.llm_summary}</pre>
        </>
      )}
    </div>
  );
}
