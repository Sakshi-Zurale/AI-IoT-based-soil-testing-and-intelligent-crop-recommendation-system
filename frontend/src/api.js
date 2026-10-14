
import axios from "axios";

const BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

const api = axios.create({
  baseURL: BASE_URL,
});

export const health = () => api.get("/health");
export const status = () => api.get("/system/status");

export const createFarmer = (d) => api.post("/farmers", d);
export const getFarmer = (id) => api.get(`/farmers/${id}`);

export const manualSoil = (d) => api.post("/soil/manual", d);
export const simulateSoil = (d) =>
  api.post("/dev/simulate-soil-reading", d);

export const latestSoil = (id) =>
  api.get("/soil/latest", {
    params: id ? { farmer_id: id } : {},
  });

export const analyzeSoil = (id) =>
  api.post("/soil/analyze", null, {
    params: { test_id: id },
  });

export const locationAnalyze = (d) => api.post("/location/analyze", d);
export const recommend = (id) =>
  api.post("/crop/recommend", null, {
    params: { test_id: id },
  });

export const history = () => api.get("/soil-tests");

export const createReport = (id) =>
  api.post(`/soil-tests/${id}/report`);

// English PDF download URL
export const reportUrl = (id) =>
  `${BASE_URL}/reports/${encodeURIComponent(id)}`;

// English + Marathi PDF download URL
export const bilingualReportUrl = (id) =>
  `${BASE_URL}/reports/${encodeURIComponent(id)}/bilingual`;

export default api;
