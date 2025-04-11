import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const location = useLocation();

  return (
    <>
      {isOpen && <div className="sidebar-backdrop" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Menu</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        <nav className="sidebar-nav">
          <ul>
            <li>
              <Link 
                to="/app/dashboard" 
                className={location.pathname === '/app/dashboard' ? 'active' : ''}
                onClick={onClose}
              >
                <span className="nav-icon">📊</span>
                Dashboard
              </Link>
            </li>
            <li>
              <Link 
                to="/app/projects" 
                className={location.pathname === '/app/projects' ? 'active' : ''}
                onClick={onClose}
              >
                <span className="nav-icon">📁</span>
                Projects
              </Link>
            </li>
            <li>
              <Link 
                to="/app/tasks" 
                className={location.pathname === '/app/tasks' ? 'active' : ''}
                onClick={onClose}
              >
                <span className="nav-icon">✅</span>
                Tasks
              </Link>
            </li>
            <li>
              <Link 
                to="/app/settings" 
                className={location.pathname === '/app/settings' ? 'active' : ''}
                onClick={onClose}
              >
                <span className="nav-icon">⚙️</span>
                Settings
              </Link>
            </li>
          </ul>
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;
