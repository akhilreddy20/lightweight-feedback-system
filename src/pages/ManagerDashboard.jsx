import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import FeedbackForm from "../components/FeedbackForm";

const ManagerDashboard = () => {
  const { employeeId } = useParams();
  const navigate = useNavigate();
  const [team, setTeam] = useState([]);

  useEffect(() => {
    const fetchTeam = async () => {
      try {
        const res = await axios.get("http://localhost:8000/feedback/team", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        console.log("Team fetched:", res.data);
        setTeam(res.data);
      } catch (err) {
        console.error("Error fetching team:", err);
      }
    };

    fetchTeam();
  }, []);

  const handleSelectEmployee = (id) => {
    navigate(`/manager-dashboard/${id}`);
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Manager Dashboard</h1>

      <p className="mb-4">Click on a team member to submit feedback:</p>

      <ul className="mb-6 space-y-2">
        {team.map((emp) => (
          <li key={emp._id} className="flex items-center justify-between border p-3 rounded">
            <div>
              <p className="font-medium">{emp.username}</p>
            </div>
            <button
              className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
              onClick={() => handleSelectEmployee(emp._id)}
            >
              Give Feedback
            </button>
          </li>
        ))}
      </ul>

      {employeeId && (
        <div className="mt-6">
          <FeedbackForm employeeId={employeeId} />
        </div>
      )}
    </div>
  );
};

export default ManagerDashboard;





/*import React from "react";
import FeedbackForm from "../components/FeedbackForm";
import { useParams } from "react-router-dom";

const ManagerDashboard = () => {
  const {employeeId} = useParams();
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-4">Manager Dashboard</h1>
      <p>View your team’s feedback overview and submit new feedback here.</p>
      <FeedbackForm employeeId={employeeId} />
    </div>
  );
};

export default ManagerDashboard;
*/