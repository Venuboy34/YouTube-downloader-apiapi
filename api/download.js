import fetch from "node-fetch";

export default async function handler(req, res) {
  // Allow CORS
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  // Handle preflight requests
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  // Get query params: url & format
  const { url, format = "mp3" } = req.query;

  if (!url) {
    return res.status(400).json({ error: "Missing 'url' parameter" });
  }

  try {
    // Example: Proxy RapidAPI YouTube downloader
    const rapidapiKey = process.env.RAPIDAPI_KEY; // store in Vercel environment
    const apiUrl = `https://youtube-info-download-api.p.rapidapi.com/ajax/download.php?format=${format}&add_info=1&url=${encodeURIComponent(
      url
    )}&audio_quality=128&allow_extended_duration=false&no_merge=false&audio_language=en`;

    const apiRes = await fetch(apiUrl, {
      headers: {
        "x-rapidapi-host": "youtube-info-download-api.p.rapidapi.com",
        "x-rapidapi-key": rapidapiKey,
      },
    });

    const data = await apiRes.json();

    // Return API JSON
    res.status(200).json(data);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error", details: err.message });
  }
}
