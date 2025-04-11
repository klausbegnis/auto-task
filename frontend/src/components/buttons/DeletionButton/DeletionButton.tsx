import '../ActionButtons.css';
import './DeletionButton.css';

interface DeleteButtonProps {
  onDeleteClick: () => void;
}

function DeleteButtonProps({ onDeleteClick }: DeleteButtonProps) {
  return (
    <div className="action-buttons-container">
      <button 
        className="action-button delete-button"
        onClick={onDeleteClick}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
}

export default DeleteButtonProps;