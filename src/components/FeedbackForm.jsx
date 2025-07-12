import React, { useState, useEffect } from "react";
import axios from "axios";

const FeedbackForm = ({ employeeId }) => {
  const [form, setForm] = useState({
    strengths: "",
    areas_to_improve: "",
    sentiment: "positive",
  });
  const [history, setHistory] = useState([]);
  const [editing, setEditing] = useState(null); // holds feedback being edited
  const [editForm, setEditForm] = useState({
    strengths: "",
    areas_to_improve: "",
    sentiment: "positive",
  });

  const fetchHistory = async () => {
    try {
      const res = await axios.get(`https://lightweight-feedback-system-backend.onrender.com/feedback/${employeeId}`, {
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
      alert("✅ Feedback submitted!");
      setForm({ strengths: "", areas_to_improve: "", sentiment: "positive" });
      fetchHistory();
    } catch (err) {
      console.error("Error submitting feedback:", err);
    }
  };

  // Edit logic
  const openEditModal = (fb) => {
    setEditing(fb);
    setEditForm({
      strengths: fb.strengths,
      areas_to_improve: fb.areas_to_improve,
      sentiment: fb.sentiment,
    });
  };

  const closeEditModal = () => {
    setEditing(null);
  };

  const handleEditChange = (e) => {
    setEditForm({ ...editForm, [e.target.name]: e.target.value });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.patch(
        `http://localhost:8000/feedback/${editing._id}/edit`,
        editForm,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      closeEditModal();
      fetchHistory();
      alert("✅ Feedback updated!");
    } catch (err) {
      console.error("Error editing feedback:", err);
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
            {history.map((fb) => (
              <li key={fb._id} className="border p-4 rounded relative">
                <p><strong>Strengths:</strong> {fb.strengths}</p>
                <p><strong>Improvements:</strong> {fb.areas_to_improve}</p>
                <p><strong>Sentiment:</strong> {fb.sentiment}</p>
                <p className="text-sm text-gray-500">
                  Submitted by {fb.manager_username} on{" "}
                  {new Date(fb.timestamp).toLocaleString()}
                </p>
                <button
                  onClick={() => openEditModal(fb)}
                  className="absolute top-2 right-2 text-blue-600 hover:underline text-sm"
                >
                  ✏️ Edit
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {editing && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded shadow-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Edit Feedback</h2>
            <form onSubmit={handleEditSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium">Strengths</label>
                <textarea
                  name="strengths"
                  value={editForm.strengths}
                  onChange={handleEditChange}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Areas to Improve</label>
                <textarea
                  name="areas_to_improve"
                  value={editForm.areas_to_improve}
                  onChange={handleEditChange}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium">Sentiment</label>
                <select
                  name="sentiment"
                  value={editForm.sentiment}
                  onChange={handleEditChange}
                  className="w-full border rounded px-3 py-2"
                >
                  <option value="positive">Positive</option>
                  <option value="neutral">Neutral</option>
                  <option value="negative">Negative</option>
                </select>
              </div>
              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={closeEditModal}
                  className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Update
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FeedbackForm;
