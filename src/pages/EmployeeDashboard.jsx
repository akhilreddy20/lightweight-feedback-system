import React, { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";

const EmployeeDashboard = () => {
  const [feedbacks, setFeedbacks] = useState([]);

  const fetchFeedback = async () => {
    try {
      const res = await axios.get("https://lightweight-feedback-system-backend.onrender.com/feedback/", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      setFeedbacks(res.data);
    } catch (err) {
      console.error("Failed to fetch feedback", err);
    }
  };

  const acknowledge = async (id) => {
    try {
      await axios.patch(`https://lightweight-feedback-system-backend.onrender.com/feedback/${id}/acknowledge`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      fetchFeedback();
    } catch (err) {
      console.error("Failed to acknowledge", err);
    }
  };

  useEffect(() => {
    fetchFeedback();
  }, []);

  return (
    <div>
      <Navbar role="Employee" />
      <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Your Feedback Timeline</h1>
      {feedbacks.length === 0 ? (
        <p>No feedback yet.</p>
      ) : (
        <ul className="space-y-4">
          {feedbacks.map((fb) => (
            <li key={fb._id} className="border p-4 rounded shadow">
              <p><strong>Strengths:</strong> {fb.strengths}</p>
              <p><strong>Areas to Improve:</strong> {fb.areas_to_improve}</p>
              <p><strong>Sentiment:</strong> {fb.sentiment}</p>
              <p className="text-gray-500 text-sm">
                From: {fb.manager_username} on {new Date(fb.timestamp).toLocaleString()}
              </p>
              {!fb.acknowledged && (
                <button
                  onClick={() => acknowledge(fb._id)}
                  className="mt-2 bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                >
                  Acknowledge
                </button>
              )}
              {fb.acknowledged && (
                <p className="text-green-600 font-semibold mt-2">✅ Acknowledged</p>
              )}
            </li>
          ))}
        </ul>
      )}
      </div>
    </div>
  );
};

export default EmployeeDashboard;


