import './ProjectsPage.css';

function ProjectsPage() {
  // Sample project data - replace with your actual data source
  const projects = [
    {
      id: 1,
      name: 'E-commerce Platform',
      description: 'AI-automated online store with dynamic pricing',
      status: 'active',
      lastUpdated: '2023-11-15',
      issues: 3,
      contributors: 5,
      techStack: ['React', 'Node.js', 'MongoDB']
    },
    {
      id: 2,
      name: 'Health Analytics Dashboard',
      description: 'Real-time health data visualization with AI predictions',
      status: 'completed',
      lastUpdated: '2023-10-28',
      issues: 0,
      contributors: 3,
      techStack: ['TypeScript', 'D3.js', 'Python']
    },
    {
      id: 3,
      name: 'Automated Documentation Generator',
      description: 'AI that writes technical docs from code comments',
      status: 'active',
      lastUpdated: '2023-11-10',
      issues: 7,
      contributors: 2,
      techStack: ['Python', 'NLP', 'Markdown']
    },
    {
      id: 4,
      name: 'Smart Code Review Assistant',
      description: 'AI that automatically reviews pull requests',
      status: 'paused',
      lastUpdated: '2023-09-05',
      issues: 12,
      contributors: 4,
      techStack: ['TypeScript', 'Machine Learning']
    }
  ];

  return (
    <div className="projects-container">
      <div className="projects-header">
        <h1>Your Projects</h1>
        <div className="projects-controls">
          <div className="search-bar">
            <svg className="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input type="text" placeholder="Search projects..." />
          </div>
          <div className="filter-controls">
            <select className="filter-select">
              <option value="all">All Statuses</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
              <option value="paused">Paused</option>
            </select>
            <button className="btn btn-primary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
              </svg>
              New Project
            </button>
          </div>
        </div>
      </div>

      <div className="projects-grid">
        {projects.map((project) => (
          <div key={project.id} className={`project-card ${project.status}`}>
            <div className="project-header">
              <h3>{project.name}</h3>
              <span className={`status-badge ${project.status}`}>
                {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
              </span>
            </div>
            <p className="project-description">{project.description}</p>
            
            <div className="project-meta">
              <div className="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Updated {project.lastUpdated}</span>
              </div>
              <div className="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{project.issues} {project.issues === 1 ? 'issue' : 'issues'}</span>
              </div>
              <div className="meta-item">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span>{project.contributors} {project.contributors === 1 ? 'contributor' : 'contributors'}</span>
              </div>
            </div>
            
            <div className="tech-stack">
              {project.techStack.map((tech, index) => (
                <span key={index} className="tech-tag">{tech}</span>
              ))}
            </div>
            
            <div className="project-actions">
              <button className="btn btn-outline btn-small">
                View Details
              </button>
              <button className="btn btn-outline btn-small">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ProjectsPage;