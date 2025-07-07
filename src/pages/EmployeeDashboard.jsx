import React, { useEffect, useState } from "react";
import axios from "axios";

const EmployeeDashboard = () => {
  const [feedbackList, setFeedbackList] = useState([]);

  const fetchFeedback = async () => {
    try {
      const res = await axios.get("http://localhost:8000/api/feedback", {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      setFeedbackList(res.data);
    } catch (err) {
      console.error("Error fetching feedback:", err);
    }
  };

  useEffect(() => {
    fetchFeedback();
  }, []);

  const acknowledge = async (id) => {
    try {
      await axios.patch(`http://localhost:8000/api/feedback/${id}/acknowledge`, null, {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      });
      fetchFeedback();
    } catch (err) {
      console.error("Error acknowledging feedback:", err);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Your Feedback Timeline</h1>
      {feedbackList.length === 0 ? (
        <p className="text-gray-500">No feedback yet.</p>
      ) : (
        <div className="space-y-4">
          {feedbackList.map((fb) => (
            <div key={fb._id} className="p-4 border rounded shadow-md">
              <p><strong>Strengths:</strong> {fb.strengths}</p>
              <p><strong>Areas to Improve:</strong> {fb.areas_to_improve}</p>
              <p><strong>Sentiment:</strong> {fb.sentiment}</p>
              <p><strong>Given by:</strong> {fb.manager_username}</p>
              <p><strong>Date:</strong> {new Date(fb.timestamp).toLocaleString()}</p>
              <p><strong>Acknowledged:</strong> {fb.acknowledged ? "Yes" : "No"}</p>
              {!fb.acknowledged && (
                <button
                  onClick={() => acknowledge(fb._id)}
                  className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Acknowledge
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default EmployeeDashboard;
