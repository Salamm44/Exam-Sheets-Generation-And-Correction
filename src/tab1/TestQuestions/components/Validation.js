import React from 'react';
import PropTypes from 'prop-types';
import { faCheck, faTimes } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import styled from 'styled-components';

const StyledValidationRule = styled.p`
  color: ${(props) => (props.validationmet ? 'green' : '#ccc')};
  margin: 0;
  text-align: left;
  display: flex;
  align-items: center;
`;

const StyledIcon = styled(FontAwesomeIcon)`
  margin-right: 10px;
  margin-left: 10px;
`;

const ValidationBlock = styled.div`
  width: 70%;
  margin-top: 16px;
`;


const Validation = ({
  areQuestionsEntered,
  areAnswersEntered,
  isCheckboxChecked,
}) => (
  <ValidationBlock>
    <div style={{ width: '100%', textAlign: 'left' }}>
      <StyledValidationRule validationmet={areQuestionsEntered}>
        <StyledIcon icon={areQuestionsEntered ? faCheck : faTimes} /> All
        questions must be entered.
      </StyledValidationRule>

      <StyledValidationRule validationmet={areAnswersEntered}>
        <StyledIcon icon={areAnswersEntered ? faCheck : faTimes} /> All
        answers must be entered.
      </StyledValidationRule>

      <StyledValidationRule validationmet={isCheckboxChecked}>
        <StyledIcon icon={isCheckboxChecked ? faCheck : faTimes} /> At least
        one checkbox in each question must be checked.
      </StyledValidationRule>
    </div>
  </ValidationBlock>
);

Validation.propTypes = {
  areQuestionsEntered: PropTypes.bool.isRequired,
  areAnswersEntered: PropTypes.bool.isRequired,
  isCheckboxChecked: PropTypes.bool.isRequired,
};

export default Validation;