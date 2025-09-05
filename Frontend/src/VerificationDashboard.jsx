import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  Legend,
} from "recharts";
import { FaHome, FaCheckCircle, FaCog } from "react-icons/fa"; // Correct Sidebar icons
import "./VerificationDashboard.css";

const VerificationDashboard = () => {
  // Dummy data
  const lineData = [
    { name: "Jan", verified: 40 },
    { name: "Feb", verified: 30 },
    { name: "Mar", verified: 50 },
    { name: "Apr", verified: 70 },
  ];

  const barData = [
    { name: "Certificates", verified: 200, rejected: 50 },
    { name: "IDs", verified: 150, rejected: 40 },
    { name: "Licenses", verified: 180, rejected: 30 },
  ];

  const pieData = [
    { name: "Verified", value: 70 },
    { name: "Rejected", value: 30 },
  ];
  const COLORS = ["#4f46e5", "#f87171"];

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>Authenex</h2>
        <ul>
          <li>
            <FaHome /> Dashboard
          </li>
          <li>
            <FaCheckCircle /> Verifications
          </li>
          <li>
            <FaCog /> Settings
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Stats Section */}
        <div className="stats-grid">
          <div className="card">
            <h3>Total Verifications</h3>
            <p>1,230</p>
          </div>
          <div className="card">
            <h3>Verified Today</h3>
            <p>45</p>
          </div>
          <div className="card">
            <h3>Pending</h3>
            <p>120</p>
          </div>
          <div className="card">
            <h3>Rejected</h3>
            <p>32</p>
          </div>
        </div>

        {/* Charts Section */}
        <div className="charts-grid">
          <div className="chart-card">
            <h3>Verification Trends</h3>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={lineData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="verified" stroke="#4f46e5" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Verification Status</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>Verification by Type</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="verified" fill="#4f46e5" />
                <Bar dataKey="rejected" fill="#f87171" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Verify Certificate Section */}
        <div className="verify-card">
          <h3>Verify Certificate</h3>
          <label className="upload-box">
            Upload PDF / JPG
            <input type="file" hidden />
          </label>

          <h3>OR</h3>

          <div className="verify-inputs">
            <input type="text" placeholder="Enter Certificate ID" />
            <input type="text" placeholder="Enter Holder Name" />
          </div>

          <button className="verify-btn">Verify</button>
        </div>
      </div>
    </div>
  );
};

export default VerificationDashboard;
