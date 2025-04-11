import '../ActionButtons.css';
import './ProjectDetailsButton.css';

interface ProjectDetailsButtonProps {
  onDetailsClick: () => void;
}

function ProjectDetailsButtonProps({ onDetailsClick }: ProjectDetailsButtonProps) {
  return (
    <div className="action-buttons-container centered">
      <button 
        className="action-button details-button"
        onClick={onDetailsClick}
      >
        View Details
      </button>
    </div>
  );
}

export default ProjectDetailsButtonProps;