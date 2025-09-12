import React, { useState } from 'react'
import Home from './Home.jsx'
import VerificationDashboard from './VerificationDashboard.jsx'

const App = () => {
  const [currentPage, setCurrentPage] = useState('home')

  return (
    <div>
      {currentPage === 'home' && (
        <div>
          <Home />
          <div className="fixed bottom-4 right-4">
            <button 
              onClick={() => setCurrentPage('dashboard')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      )}
      
      {currentPage === 'dashboard' && (
        <div>
          <VerificationDashboard />
          <div className="fixed top-4 left-4">
            <button 
              onClick={() => setCurrentPage('home')}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
            >
              ← Back to Home
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App