import './AddButton.css';

interface AddButtonProps {
  onClick: () => void;
  text?: string;
  className?: string;
}

function AddButton({ onClick, text}: AddButtonProps) {
  return (
    <button className={`btn btn-primary add-button}`} onClick={onClick}>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
      </svg>
      {text && <span>{text}</span>}
    </button>
  );
}

export default AddButton;
