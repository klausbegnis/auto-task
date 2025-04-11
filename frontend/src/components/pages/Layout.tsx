import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from '../Sidebar/Sidebar';
import './Layout.css';

const Layout: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <div className="layout">
      <Sidebar 
        isOpen={isSidebarOpen} 
        onClose={() => setIsSidebarOpen(false)} 
      />
      
      <div className="main-content">
        <header className="header">
          <button 
            className="menu-button"
            onClick={() => setIsSidebarOpen(true)}
          >
            ☰
          </button>
          <h1>AutoTask</h1>
        </header>
        <div className="content">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default Layout; 