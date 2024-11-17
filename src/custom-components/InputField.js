import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faRedo } from '@fortawesome/free-solid-svg-icons';
import './InputField.css'; // import the CSS file
import PropTypes from 'prop-types';

const InputField = ({ type, name, placeholder, initialValue, propValue, error, handleInputChange, hint, disabled, readOnly }) => {
    const [value, setValue] = useState(propValue);

    // Update the local state when propValue changes
    useEffect(() => {
        setValue(propValue);
    }, [propValue]);

    const handleInputChangeLocal = (e) => {
        const newValue = e.target.value;
        const newError = (isNotNullOrUndefined(newValue) && type !== 'number' && /^\d+$/.test(newValue)) || 
                         (isNotNullOrUndefined(newValue) && type === 'number' && (!/^\d{1,2}$/.test(newValue))) || 
                         (error && isNotNullOrUndefined(newValue) && !/^\d+$/.test(newValue));
        setValue(newValue);
        handleInputChange(e, newError);
    }

    const handleResetDate = () => {
        setValue('');
    }

    return (
        <div className="input-field-container">
            <div className={type === 'date' ? "date-input-container" : "normal-input-container"}>
                <input 
                    type={type} 
                    name={name} 
                    placeholder={placeholder} 
                    value={value}
                    className="creation-input" 
                    style={{ borderColor: (value && type !== 'number' && /^\d+$/.test(value)) ? '1px solid red' : 'none !important' }} 
                    onChange={handleInputChangeLocal} 
                    readOnly={readOnly}
                    disabled={disabled}
                />
                {type === 'date' && <FontAwesomeIcon icon={faRedo} onClick={handleResetDate} />}
                {isNotNullOrUndefined(value) && type !== 'number' && /^\d+$/.test(value) && <p className="error-message">{placeholder} should not be a number</p>}
                {isNotNullOrUndefined(value) && type === 'number' && (!/^\d{1,3}$/.test(value)) && <p className="error-message">{placeholder} should be between one and three-digit number</p>}
                {error && isNotNullOrUndefined(value) && !/^\d+$/.test(value) && <p className="warning-message">{placeholder} should be at least 3 letters</p>}
                {disabled && hint && <p className="warning-message">{hint}</p>}
            </div>
        </div>
    );
}

function isNotNullOrUndefined(value) {
    return value !== null && value !== undefined;
}

InputField.propTypes = {
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    placeholder: PropTypes.string.isRequired,
    initialValue: PropTypes.string,
    propValue: PropTypes.string,
    error: PropTypes.bool,
    handleInputChange: PropTypes.func.isRequired,
    disabled: PropTypes.bool,
    readOnly: PropTypes.bool,
    hint: PropTypes.string,
  };
  

export default InputField;