import './ProjectsPage.css';
import type { Project } from '../../cards/ProjectCards';
import ProjectCards from '../../cards/ProjectCards';
import NewProjectCard from '../../cards/NewProjectCard';
import AddButton from '../../buttons/AddButton/AddButton';

function ProjectsPage() {
  // Sample project data - replace with your actual data source
  const projects: Project[] = [
    {
      id: 1,
      name: 'Sample card',
      description: 'Sample description',
      status: 'active',
      lastUpdated: '2023-11-15',
      issues: 3,
      contributors: 5,
      techStack: ['React', 'Node.js', 'MongoDB']
    }
  ];

  const handleViewDetails = (projectId: number) => {
    // Your view details logic here
    console.log(`Viewing details for project ${projectId}`);
  };
  
  const handleDeleteProject = (projectId: number) => {
    // Your delete logic here
    console.log(`Deleting project ${projectId}`);
  };

  const handleNewProject = () => {
    // Your new project logic here
    console.log('Creating new project');
  };

  return (
    <>
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
              <AddButton onClick={handleNewProject} text="New Project" />
            </div>
          </div>
        </div>

        <div className="projects-grid">
          {projects.map((project) => (
              <ProjectCards 
                  project={project}
                  handleViewDetails={handleViewDetails}
              />
          ))}
          <NewProjectCard onClick={handleNewProject} />
        </div>
      </div>
    </>
  );
}

export default ProjectsPage;