import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import QuestionForm from './components/QuestionForm';
import useLocalStorage from '../hooks/useLocalStorage';

const StyledDiv = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
`;

  const StyledRowDiv = styled.div`
    display: flex;
    flex-direction: row;
    justify-content: center
    width: 100%;
  `;

const StyledP = styled.p`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  font-size: 20px;
  color: #333;
  margin-top: 0px;
  margin-bottom: 20px;
  margin-right: 20px;
  padding: 10px;
  border-radius: 5px;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12), 0 1px 2px rgba(0, 0, 0, 0.24);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  width: 150px;
  &:hover {
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
  }
`;

const AddButton = styled.button`
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #8C0303;
  color: white;
  font-size: 20px;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  margin-right: 10px;

  &:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
`;

const ButtonContainer = styled.div`
  display: flex;
`;

const TestQuestions = () => {
  const [form, setForm] = useState(JSON.parse(localStorage.getItem('form')) || { numQuestions: 0 });
  const [numQuestions, setNumQuestions] = useState(form.numQuestions); 
  const [numAnswers, setNumAnswers] = useState(form.numAnswers); 

  useEffect(() => {
    setNumQuestions(form.numQuestions)
  }, [form]);

  //  retrieve numQuestions and numAnswers from localStorage 
  useEffect(() => {
    const storedForm = JSON.parse(localStorage.getItem('form'));
    if (storedForm) {
      if (!isNaN(Number(storedForm.numQuestions))) {
        setNumQuestions(Number(storedForm.numQuestions));
      }

      if (!isNaN(Number(storedForm.numAnswers))) {
        setNumAnswers(Number(storedForm.numAnswers));
      }
    }
  }, []);

  const increaseQuestionCount = () => {
    setNumQuestions(numQuestions + 1);
  };

  return (
    <StyledDiv>
      <StyledRowDiv>
        <StyledP>
          Questions: {numQuestions}
          <ButtonContainer>
            <AddButton onClick={increaseQuestionCount} disabled="true">+</AddButton>
          </ButtonContainer>
        </StyledP>
        <StyledP>
          Answers: {numAnswers}
          <ButtonContainer>
            <AddButton onClick={increaseQuestionCount} disabled="true" >+</AddButton>
            <AddButton onClick={increaseQuestionCount} disabled="true" >-</AddButton>
          </ButtonContainer>
        </StyledP>

      </StyledRowDiv> 
        <QuestionForm formProp={form} updateForm={setForm} numQuestions={numQuestions} numAnswers={numAnswers} />
    </StyledDiv>
  );
};

export default TestQuestions;
