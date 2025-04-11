import './ProjectCards.css';
import ProjectDetailsButton from '../buttons/ProjectDetailsButton/ProjectDetailsButton';

export interface Project {
  id: number;
  name: string;
  description: string;
  status: 'active' | 'completed' | 'paused';
  lastUpdated: string;
  issues: number;
  contributors: number;
  techStack: string[];
}

interface ProjectCardsProps {
  project: Project;
  handleViewDetails: (id: number) => void;
}

function ProjectCards({ project, handleViewDetails }: ProjectCardsProps) {
    return (
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
            <ProjectDetailsButton 
                onDetailsClick={() => handleViewDetails(project.id)}
            />
        </div>
    )
} 

export default ProjectCards;