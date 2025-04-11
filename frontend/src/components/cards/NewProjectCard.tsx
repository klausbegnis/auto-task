import './NewProjectCard.css';

type Props = {
  onClick: () => void;
};

const NewProjectCard = ({ onClick }: Props) => {
  return (
    <div className="new-project-card" onClick={onClick}>
      <div className="plus-icon">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
        </svg>
      </div>
      <p>Add New Project</p>
    </div>
  );
};

export default NewProjectCard;
