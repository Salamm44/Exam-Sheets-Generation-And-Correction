import React, { useState } from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';

const StyledAnswerBlock = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
`;

const StyledCheckbox = styled.input.attrs({ type: 'checkbox' })`
  width: 20px;
  height: 20px;
  margin: 10px;
  align-self: center;
`;

const StyledInput = styled.input`
  display: flex;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
`;



const Answer = ({ answer, qIndex, aIndex, handleAnswerChange }) => (
  <StyledAnswerBlock key={`question-block-${qIndex}`}>
    <StyledInput
      type="text"
      value={answer.text}
      onChange={(event) =>
        handleAnswerChange(qIndex, aIndex, event.target.value, answer.isCorrect)
      }
      placeholder="Enter answer"
    />
    <StyledCheckbox
      checked={answer.isCorrect}
      onChange={(event) =>
        handleAnswerChange(qIndex, aIndex, answer.text, event.target.checked)
      }
    />
  </StyledAnswerBlock>
);

Answer.propTypes = {
  answer: PropTypes.shape({
    text: PropTypes.string,
    isCorrect: PropTypes.bool,
  }).isRequired,
  qIndex: PropTypes.number.isRequired,
  aIndex: PropTypes.number.isRequired,
  handleAnswerChange: PropTypes.func.isRequired,
};

export default Answer;