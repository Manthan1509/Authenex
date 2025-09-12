import React, { useState, useEffect } from "react";
import { FaHome, FaCheckCircle, FaCog } from "react-icons/fa";
import { api } from "./services/api";
import "./VerificationDashboard.css";

// Simple i18n implementation
const translations = {
  en: {
    dashboard: "Dashboard",
    verifications: "Verifications",
    settings: "Settings",
    totalVerifications: "Total Verifications",
    verifiedToday: "Verified Today",
    pending: "Pending",
    rejected: "Rejected",
    systemStatus: "System Status",
    certificateOperations: "Certificate Operations",
    uploadCertificate: "Upload Certificate (PDF/JPG)",
    parseCertificate: "Parse Certificate",
    storeOnBlockchain: "Store on Blockchain",
    enterCertificateHash: "Enter Certificate Hash",
    enterHolderName: "Enter Holder Name",
    verifyByHash: "Verify by Hash",
    processing: "Processing...",
    result: "Result:"
  }
};

const useTranslation = (lang = 'en') => {
  return translations[lang] || translations.en;
};

const VerificationDashboard = () => {
  const [file, setFile] = useState(null);
  const [certificateHash, setCertificateHash] = useState('');
  const [holderName, setHolderName] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [healthStatus, setHealthStatus] = useState(null);
  const t = useTranslation();

  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const health = await api.healthCheck();
      setHealthStatus(health);
    } catch (error) {
      console.error('Health check failed:', error);
    }
  };

  const handleFileUpload = (event) => {
    setFile(event.target.files[0]);
    setResult(null);
  };

  const handleParseCertificate = async () => {
    if (!file) return;
    
    setLoading(true);
    try {
      const response = await api.parseCertificate(file);
      setResult(response);
    } catch (error) {
      setResult({ error: 'Failed to parse certificate' });
    }
    setLoading(false);
  };

  const handleStoreCertificate = async () => {
    if (!file) return;
    
    setLoading(true);
    try {
      const response = await api.storeCertificateBlockchain(file, '0x1234567890123456789012345678901234567890');
      setResult(response);
    } catch (error) {
      setResult({ error: 'Failed to store certificate' });
    }
    setLoading(false);
  };

  const handleVerifyById = async () => {
    if (!certificateHash) return;
    
    setLoading(true);
    try {
      const response = await api.getCertificateBlockchain(certificateHash);
      setResult(response);
    } catch (error) {
      setResult({ error: 'Failed to verify certificate' });
    }
    setLoading(false);
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>Authenex</h2>
        <ul>
          <li>
            <FaHome /> {t.dashboard}
          </li>
          <li>
            <FaCheckCircle /> {t.verifications}
          </li>
          <li>
            <FaCog /> {t.settings}
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="main-content">
        {/* Stats Section */}
        <div className="stats-grid">
          <div className="card">
            <h3>{t.totalVerifications}</h3>
            <p>1,230</p>
          </div>
          <div className="card">
            <h3>{t.verifiedToday}</h3>
            <p>45</p>
          </div>
          <div className="card">
            <h3>{t.pending}</h3>
            <p>120</p>
          </div>
          <div className="card">
            <h3>{t.rejected}</h3>
            <p>32</p>
          </div>
        </div>

        {/* System Status */}
        <div className="chart-card">
          <h3>{t.systemStatus}</h3>
          {healthStatus && (
            <div className="status-grid">
              <div className={`status-item ${healthStatus.status === 'healthy' ? 'healthy' : 'unhealthy'}`}>
                API Status: {healthStatus.status}
              </div>
              <div className={`status-item ${healthStatus.blockchain_connected ? 'healthy' : 'unhealthy'}`}>
                Blockchain: {healthStatus.blockchain_connected ? 'Connected' : 'Disconnected'}
              </div>
              <div className={`status-item ${healthStatus.ai_models_loaded?.certificate_parser ? 'healthy' : 'unhealthy'}`}>
                AI Parser: {healthStatus.ai_models_loaded?.certificate_parser ? 'Loaded' : 'Mock'}
              </div>
            </div>
          )}
        </div>

        {/* Verify Certificate Section */}
        <div className="verify-card">
          <h3>{t.certificateOperations}</h3>
          
          <div className="upload-section">
            <label className="upload-box">
              {t.uploadCertificate}
              <input type="file" onChange={handleFileUpload} accept=".pdf,.jpg,.jpeg,.png" />
            </label>
            {file && <p>Selected: {file.name}</p>}
            
            <div className="button-group">
              <button 
                className="verify-btn" 
                onClick={handleParseCertificate}
                disabled={!file || loading}
              >
                {t.parseCertificate}
              </button>
              <button 
                className="verify-btn" 
                onClick={handleStoreCertificate}
                disabled={!file || loading}
              >
                {t.storeOnBlockchain}
              </button>
            </div>
          </div>

          <div className="divider">OR</div>

          <div className="verify-inputs">
            <input 
              type="text" 
              placeholder={t.enterCertificateHash}
              value={certificateHash}
              onChange={(e) => setCertificateHash(e.target.value)}
            />
            <input 
              type="text" 
              placeholder={t.enterHolderName}
              value={holderName}
              onChange={(e) => setHolderName(e.target.value)}
            />
            <button 
              className="verify-btn" 
              onClick={handleVerifyById}
              disabled={!certificateHash || loading}
            >
              {loading ? t.processing : t.verifyByHash}
            </button>
          </div>

          {/* Results */}
          {result && (
            <div className="result-section">
              <h4>{t.result}</h4>
              <pre className="result-display">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VerificationDashboard;
