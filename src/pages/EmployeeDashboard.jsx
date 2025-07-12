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
      await axios.patch(`http://localhost:8000/feedback/${id}/acknowledge`, {}, {
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



/*import React, { useEffect, useState } from "react";
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
*/
