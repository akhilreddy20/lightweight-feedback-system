import React, { useState, useEffect } from "react";
import axios from "axios";

const FeedbackForm = ({ employeeId }) => {
  const [form, setForm] = useState({
    strengths: "",
    areas_to_improve: "",
    sentiment: "positive",
  });
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/feedback/${employeeId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setHistory(res.data);
    } catch (err) {
      console.error("Error fetching feedback history:", err);
    }
  };

  useEffect(() => {
    if (employeeId) {
      fetchHistory();
    }
  }, [employeeId]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();

  if (!employeeId) {
    console.error("Cannot submit: employeeId is undefined");
    return;
  }

  try {
    await axios.post(
      `http://localhost:8000/feedback/${employeeId}`,
      form,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    alert("Feedback submitted!");
    setForm({ strengths: "", areas_to_improve: "", sentiment: "positive" });
    fetchHistory(); // Refresh history after submission
  } catch (err) {
    console.error("Error submitting feedback:", err);
  }
};


  return (
    <div className="p-6 bg-white rounded shadow max-w-xl mx-auto">
      <h2 className="text-xl font-semibold mb-4">Submit Feedback</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium">Strengths</label>
          <textarea
            name="strengths"
            value={form.strengths}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Areas to Improve</label>
          <textarea
            name="areas_to_improve"
            value={form.areas_to_improve}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium">Sentiment</label>
          <select
            name="sentiment"
            value={form.sentiment}
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          >
            <option value="positive">Positive</option>
            <option value="neutral">Neutral</option>
            <option value="negative">Negative</option>
          </select>
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Submit Feedback
        </button>
      </form>

      <div className="mt-8">
        <h3 className="text-lg font-semibold mb-2">Feedback History</h3>
        {history.length === 0 ? (
          <p className="text-gray-500">No feedback submitted yet.</p>
        ) : (
          <ul className="space-y-4">
            {history.map((fb, idx) => (
              <li key={idx} className="border p-4 rounded">
                <p><strong>Strengths:</strong> {fb.strengths}</p>
                <p><strong>Improvements:</strong> {fb.areas_to_improve}</p>
                <p><strong>Sentiment:</strong> {fb.sentiment}</p>
                <p className="text-sm text-gray-500">
                  Submitted by {fb.manager_username} on{" "}
                  {new Date(fb.timestamp).toLocaleString()}
                </p>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default FeedbackForm;
