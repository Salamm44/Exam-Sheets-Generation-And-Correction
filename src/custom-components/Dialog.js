import React from 'react';

const Dialog = ({ title, message, onClose }) => {
  return (
    <div className="dialog">
      <h2>{title}</h2>
      <p>{message}</p>
      <button onClick={onClose}>Close</button>
    </div>
  );
};

export default Dialog;