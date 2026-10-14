
import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  useNavigate,
  useLocation,
  Routes,
  Route,
} from "react-router-dom";
import {
  LayoutDashboard,
  UserRound,
  FlaskConical,
  BrainCircuit,
  FileText,
  History as HistoryIcon,
  Settings,
  Wifi,
  RefreshCw,
  ChevronRight,
} from "lucide-react";
import * as api from "./api";
import "./index.css";

const navItems = [
  ["/", "Dashboard", LayoutDashboard],
  ["/farmer", "Farmer Details", UserRound],
  ["/test", "Soil Testing", FlaskConical],
  ["/analysis", "Soil Analysis", BrainCircuit],
  ["/recommendation", "AI Recommendation", BrainCircuit],
  ["/reports", "Reports", FileText],
  ["/history", "Test History", HistoryIcon],
  ["/settings", "Settings", Settings],
];

function Shell({ children }) {
  const nav = useNavigate();
  const loc = useLocation();
  const [online, setOnline] = useState(false);
  const [farmer, setFarmer] = useState(null);

  useEffect(() => {
    api
      .status()
      .then((r) => {
        setOnline(true);
        if (r.data.farmer_configured) {
          const id = localStorage.getItem("farmerId");
          if (id) {
            api
              .getFarmer(id)
              .then((x) => setFarmer(x.data))
              .catch(() => {});
          }
        }
      })
      .catch(() => setOnline(false));
  }, [loc.pathname]);

  return (
    <div className="app">
      <header className="header">
        <div>
          <span className="brand">KrushiAI</span>
          <span className="badge">AI-IoT Soil Intelligence</span>
        </div>
        <div className="status">
          {online ? "API Online" : "API Offline"} ·{" "}
          {farmer ? farmer.name : "Farmer Not Configured"}
        </div>
      </header>

      <div className="layout">
        <aside className="sidebar">
          {navItems.map(([path, title, Icon]) => (
            <button
              key={path}
              className={"navbtn " + (loc.pathname === path ? "active" : "")}
              onClick={() => nav(path)}
            >
              <Icon
                size={17}
                style={{ verticalAlign: "middle", marginRight: 9 }}
              />
              {title}
            </button>
          ))}
        </aside>

        <main className="main">{children}</main>
      </div>

      <nav className="bottom">
        {navItems.slice(0, 5).map(([path, title, Icon]) => (
          <button
            key={path}
            className={loc.pathname === path ? "active" : ""}
            onClick={() => nav(path)}
          >
            <Icon size={18} />
            <br />
            {title.split(" ")[0]}
          </button>
        ))}
      </nav>
    </div>
  );
}

function Dashboard() {
  const nav = useNavigate();
  const [s, setS] = useState(null);

  useEffect(() => {
    api.status().then((r) => setS(r.data)).catch(() => setS(null));
  }, []);

  return (
    <>
      <h1>Dashboard</h1>
      <p className="muted">
        AI-IoT based soil testing and crop recommendation.
      </p>

      <div className="section">
        <div className="workflow">
          {["Farmer", "Test", "Soil", "AI Engine", "Report"].map(
            (x, i) => (
              <div className="stage" key={x}>
                <strong>
                  {i + 1}. {x}
                </strong>
                <span>
                  {i === 0 ? "Profile" : i === 1 ? "Input" : "Pending"}
                </span>
              </div>
            )
          )}
        </div>
      </div>

      <div className="grid grid4 section">
        <Stat
          title="Farmer Details"
          value={s?.farmer_configured ? "Configured" : "Not Configured"}
          icon={<UserRound />}
        />
        <Stat title="IoT Gateway" value="Disconnected" icon={<Wifi />} />
        <Stat
          title="Soil Data"
          value="Waiting for input"
          icon={<FlaskConical />}
        />
        <Stat
          title="AI Analysis"
          value="Not Started"
          icon={<BrainCircuit />}
        />
      </div>

      <div className="card section">
        <div className="sectiontitle">
          <div>
            <h3>Start Soil Testing Workflow</h3>
            <div className="muted">
              Enter farmer details, collect soil data, analyse it and generate
              recommendations.
            </div>
          </div>
          <button
            className="btn"
            onClick={() =>
              nav(s?.farmer_configured ? "/test" : "/farmer")
            }
          >
            Start New Soil Test{" "}
            <ChevronRight size={15} style={{ verticalAlign: "middle" }} />
          </button>
        </div>
      </div>

      <div className="grid grid2 section">
        <div className="card">
          <h3>Recent Test Records</h3>
          <div className="empty">No soil tests recorded yet.</div>
        </div>
        <div className="card">
          <h3>Hardware Topology</h3>
          <p className="muted">
            NPK Sensor → RS485/MAX485 → ESP32 → Wi-Fi → KrushiAI Backend
          </p>
          <div className="tag">NPK</div>
          <div className="tag">Moisture</div>
          <div className="tag">Temperature</div>
          <div className="tag">Humidity</div>
        </div>
      </div>
    </>
  );
}

function Stat({ title, value, icon }) {
  return (
    <div className="card">
      <div className="muted">
        {icon} {title}
      </div>
      <div className="value">{value}</div>
    </div>
  );
}

function Farmer() {
  const [form, setForm] = useState({
    name: "",
    mobile: "",
    village: "",
    taluka: "",
    district: "",
    state: "",
    farm_name: "",
    preferred_crop: "",
  });
  const [msg, setMsg] = useState("");

  const save = async (e) => {
    e.preventDefault();
    try {
      const r = await api.createFarmer(form);
      localStorage.setItem("farmerId", r.data.id);
      setMsg("Farmer profile saved successfully.");
    } catch (e) {
      setMsg(e.response?.data?.detail || "Could not save farmer.");
    }
  };

  const field = (k) => (
    <div className="field">
      <label>
        {k.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
      </label>
      <input
        value={form[k]}
        onChange={(e) => setForm({ ...form, [k]: e.target.value })}
        required={!["farm_name", "preferred_crop"].includes(k)}
      />
    </div>
  );

  return (
    <>
      <h1>Farmer Details</h1>
      <p className="muted">
        Create the farmer profile used by soil tests and reports.
      </p>
      <form className="card" onSubmit={save}>
        <div className="formgrid">
          {Object.keys(form).map((k) =>
            React.cloneElement(field(k), { key: k })
          )}
        </div>
        {msg && (
          <div
            className={
              "alert " + (msg.includes("success") ? "success" : "error")
            }
            style={{ marginTop: 15 }}
          >
            {msg}
          </div>
        )}
        <div className="actions">
          <button className="btn">Save Farmer Profile</button>
        </div>
      </form>
    </>
  );
}

function TestPage() {
  const farmerId = localStorage.getItem("farmerId");
  const [mode, setMode] = useState("manual");
  const [data, setData] = useState({
    farmer_id: Number(farmerId) || 0,
    nitrogen: "",
    phosphorus: "",
    potassium: "",
    soil_moisture: "",
    air_temperature: "",
    humidity: "",
  });
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();

    if (!farmerId) {
      setMsg("Create a farmer profile first.");
      return;
    }

    try {
      const r =
        mode === "manual"
          ? await api.manualSoil({
              ...data,
              farmer_id: Number(farmerId),
            })
          : await api.simulateSoil({
              farmer_id: Number(farmerId),
            });

      localStorage.setItem("testId", r.data.test_id);
      setMsg(`Test ${r.data.test_id} saved.`);
      nav("/analysis");
    } catch (e) {
      setMsg(e.response?.data?.detail || "Unable to save test.");
    }
  };

  const field = (k, label) => (
    <div className="field" key={k}>
      <label>{label}</label>
      <input
        type="number"
        step="any"
        required
        value={data[k]}
        onChange={(e) => setData({ ...data, [k]: e.target.value })}
      />
    </div>
  );

  return (
    <>
      <h1>Soil Testing</h1>
      <p className="muted">
        Choose developer simulation or enter known soil values manually.
      </p>

      <div className="actions">
        <button
          type="button"
          className={"btn " + (mode === "manual" ? "" : "secondary")}
          onClick={() => setMode("manual")}
        >
          Manual Input
        </button>
        <button
          type="button"
          className={"btn " + (mode === "sim" ? "" : "secondary")}
          onClick={() => setMode("sim")}
        >
          Developer Sensor Simulator
        </button>
      </div>

      {mode === "manual" ? (
        <form className="card section" onSubmit={submit}>
          <div className="formgrid">
            {field("nitrogen", "Nitrogen (N)")}
            {field("phosphorus", "Phosphorus (P)")}
            {field("potassium", "Potassium (K)")}
            {field("soil_moisture", "Soil Moisture (%)")}
            {field("air_temperature", "Air Temperature (°C)")}
            {field("humidity", "Humidity (%)")}
          </div>
          <div className="muted" style={{ marginTop: 12 }}>
            Data Source: Manual Input
          </div>
          <div className="actions">
            <button className="btn">Save Soil Test</button>
          </div>
        </form>
      ) : (
        <div className="card section">
          <h3>Developer-only simulator</h3>
          <p className="muted">
            This creates clearly labelled simulated data for local development.
            It is not live sensor data.
          </p>
          <button type="button" className="btn" onClick={submit}>
            Generate Test Reading
          </button>
        </div>
      )}

      {msg && (
        <div className="alert" style={{ marginTop: 15 }}>
          {msg}
        </div>
      )}
    </>
  );
}

function Analysis() {
  const testId = localStorage.getItem("testId");
  const [a, setA] = useState(null);
  const [msg, setMsg] = useState("");

  const run = async () => {
    if (!testId) return;

    try {
      const r = await api.analyzeSoil(testId);
      setA(r.data);
      setMsg("");
    } catch (e) {
      setMsg(e.response?.data?.detail || "Analysis failed.");
    }
  };

  useEffect(() => {
    run();
  }, []);

  return (
    <>
      <h1>Soil Analysis</h1>
      <p className="muted">
        Configured reference-range analysis for the recorded test.
      </p>

      {!testId ? (
        <div className="alert">
          No active test. Create a soil test first.
        </div>
      ) : (
        <>
          <button className="btn" onClick={run}>
            <RefreshCw size={15} /> Run Analysis
          </button>
          <div className="grid grid3 section">
            {a &&
              Object.entries(a.parameters).map(([k, v]) => (
                <div className="card" key={k}>
                  <h3>{k.replaceAll("_", " ")}</h3>
                  <div className="value">{v.value}</div>
                  <span className="tag">{v.status}</span>
                  <p className="muted">{v.interpretation}</p>
                </div>
              ))}
          </div>
          {msg && <div className="alert error">{msg}</div>}
        </>
      )}
    </>
  );
}

function Recommendation() {
  const testId = localStorage.getItem("testId");
  const [r, setR] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const run = async () => {
    if (!testId) {
      setMsg("No active test.");
      return;
    }

    setLoading(true);
    setMsg("");

    try {
      const x = await api.recommend(testId);
      setR(x.data);
    } catch (e) {
      setMsg(e.response?.data?.detail || "Recommendation failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h1>AI Crop Recommendation</h1>
      <p className="muted">
        Random Forest prediction + local agricultural knowledge retrieval +
        structured explanation.
      </p>

      <button className="btn" disabled={loading} onClick={run}>
        {loading ? "Analysing..." : "Run AI Recommendation"}
      </button>

      {msg && <div className="alert error section">{msg}</div>}

      {r && (
        <>
          <div className="alert section">
            {r.preferred_crop_note || "No preferred crop supplied."}
          </div>
          <div className="grid grid2">
            {r.recommendations.map((x) => (
              <div className="rec" key={x.crop}>
                <h3>{x.crop}</h3>
                <div className="tag">
                  Model probability: {(x.ml_probability * 100).toFixed(1)}%
                </div>
                <div className="tag">{x.suitability}</div>
                <p className="muted">{x.soil_compatibility}</p>
                <p className="muted">{x.location_compatibility}</p>
                <p className="muted">{x.weather_compatibility}</p>
                <p className="muted">{x.preference_compatibility}</p>
                <p>{x.explanation}</p>
              </div>
            ))}
          </div>
          <div className="actions section">
            <button className="btn" onClick={() => nav("/reports")}>
              Continue to Report
            </button>
          </div>
        </>
      )}
    </>
  );
}

/* Reports: English PDF + bilingual English/Marathi PDF */
function Reports() {
  const testId = localStorage.getItem("testId");
  const [msg, setMsg] = useState("");
  const [error, setError] = useState(false);
  const [englishUrl, setEnglishUrl] = useState("");
  const [bilingualUrl, setBilingualUrl] = useState("");

  const create = () => {
    if (!testId) {
      setError(true);
      setMsg("No active test. Please create a soil test first.");
      return;
    }

    setError(false);

    try {
      // Both GET endpoints have already been verified to return PDF files.
      // Show their download links directly instead of relying on the POST.
      setEnglishUrl(api.reportUrl(testId));
      setBilingualUrl(api.bilingualReportUrl(testId));
      setMsg("Your report download options are ready. Choose a PDF below.");
    } catch (e) {
      console.error("Report link error:", e);
      setError(true);
      setMsg("Unable to prepare report links. Check your API configuration.");
    }
  };

  return (
    <>
      <h1>Soil Testing Reports</h1>
      <p className="muted">
        Download your KrushiAI soil testing report in English or bilingual
        English + Marathi.
      </p>

      {!testId ? (
        <div className="alert">
          No active test. Please create a soil test first.
        </div>
      ) : (
        <>
          <div className="card section">
            <FileText size={28} />
            <h3>Generate Soil Report</h3>
            <p className="muted">
              Choose a report format for your saved soil test and
              recommendations.
            </p>

            <button type="button" className="btn" onClick={create}>
              Show PDF Download Options
            </button>

            {msg && (
              <div
                className={"alert " + (error ? "error" : "success")}
                style={{ marginTop: 15 }}
              >
                {msg}
              </div>
            )}
          </div>

          {englishUrl && bilingualUrl && (
            <div className="grid grid2 section">
              <div className="card">
                <FileText size={25} />
                <h3>English Report</h3>
                <p className="muted">
                  Soil readings, analysis, crop recommendations and notices
                  in English.
                </p>
                <a
                  className="btn"
                  href={englishUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download English PDF
                </a>
              </div>

              <div className="card">
                <FileText size={25} />
                <h3>English + मराठी</h3>
                <p className="muted">
                  A bilingual PDF for farmers who prefer Marathi along with
                  English.
                </p>
                <a
                  className="btn"
                  href={bilingualUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download English + Marathi PDF
                </a>
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}

function History() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.history().then((r) => setRows(r.data)).catch(() => {});
  }, []);

  return (
    <>
      <h1>Test History</h1>
      <p className="muted">Saved soil tests from the database.</p>
      <div className="card">
        {rows.length === 0 ? (
          <div className="empty">No soil tests recorded yet.</div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Test ID</th>
                <th>Source</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((x) => (
                <tr key={x.id}>
                  <td>{x.test_id}</td>
                  <td>{x.input_source}</td>
                  <td>{new Date(x.created_at).toLocaleString()}</td>
                  <td>{x.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

function SettingsPage() {
  return (
    <>
      <h1>Settings</h1>
      <div className="card">
        <h3>System</h3>
        <p className="muted">API: http://localhost:8000</p>
        <p className="muted">
          Database: SQLite by default. MySQL can be configured through
          DATABASE_URL.
        </p>
        <h3>Hardware</h3>
        <p className="muted">
          ESP32 → RS485/MAX485 → NPK + DHT + soil moisture
        </p>
        <h3>Data policy</h3>
        <p className="muted">
          No farmer or sensor values are fabricated. The bundled ML file is
          explicitly a demo training dataset.
        </p>
      </div>
    </>
  );
}

function Placeholder({ title }) {
  return (
    <>
      <h1>{title}</h1>
      <div className="card empty">
        Use the workflow: Farmer → Soil Testing → Soil Analysis → AI
        Recommendation → Reports.
      </div>
    </>
  );
}

function App() {
  return (
    <Shell>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/farmer" element={<Farmer />} />
        <Route path="/test" element={<TestPage />} />
        <Route path="/analysis" element={<Analysis />} />
        <Route path="/recommendation" element={<Recommendation />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/history" element={<History />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </Shell>
  );
}

createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
