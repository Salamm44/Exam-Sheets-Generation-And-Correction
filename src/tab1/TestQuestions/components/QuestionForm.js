import React, { useState, useEffect, useCallback } from 'react';
import { faSave } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { toast } from 'react-toastify';
import PropTypes from 'prop-types';
import useLocalStorage from '../../hooks/useLocalStorage';

import Answer from './Answer';
import Validation from './Validation';

import * as Styled from './QuestionFormStyles';

const Question = ({
  question,
  qIndex,
  handleQuestionChange,
  answers,
  handleAnswerChange,
  handleRemoveQuestion,
}) => (
  <Styled.QuestionBlock key={`question-block-${qIndex}`}>
    <Styled.H3>Question {qIndex + 1}:</Styled.H3>
    <Styled.QuestionRow>
    <Styled.Input
      type="text"
      value={question.text}
      onChange={(event) => handleQuestionChange(qIndex, event.target.value)}
      placeholder="Enter question"
    />
    <Styled.RemoveButton onClick={() => handleRemoveQuestion(qIndex)}>X</Styled.RemoveButton>
    </Styled.QuestionRow>
    {answers[qIndex] &&
      // eslint-disable-next-line react/prop-types
      answers[qIndex].map((answer, aIndex) => (
        <Answer
          key={`answer-${qIndex}-${aIndex}`}
          answer={answer}
          qIndex={qIndex}
          aIndex={aIndex}
          handleAnswerChange={handleAnswerChange}
        />
      ))}
  </Styled.QuestionBlock>
);

const QuestionForm = ({ numQuestions = 0, numAnswers = 0, formProp, updateForm}) => {
  const [questions, setQuestions] = useLocalStorage('questions', []);
  const [answers, setAnswers] = useLocalStorage('answers', []);
  const [areQuestionsEntered, setAreQuestionsEntered] = useState(false);
  const [areAnswersEntered, setAreAnswersEntered] = useState(false);
  const [isCheckboxChecked, setIsCheckboxChecked] = useState(false);

  const [form, setForm] = useLocalStorage('form', { numQuestions: 0});

  useEffect(() => {
    setForm(formProp);
  }, [formProp, setForm]);


  useEffect(() => {
    // Only set initialQuestions and initialAnswers if local storage is empty
    if (questions.length === 0 && answers.length === 0) {
      const initialQuestions = Array.from({ length: numQuestions }, () => ({
        text: '',
      }));

      const initialAnswers = Array.from({ length: numQuestions }, () =>
        Array.from({ length: numAnswers }, () => ({
          text: '',
          isCorrect: false,
        })),
      );

      setQuestions(initialQuestions);
      setAnswers(initialAnswers);
    }
  }, [numQuestions, numAnswers, setQuestions, setAnswers]);

  useEffect(() => {
    setAreQuestionsEntered(questions.every((question) => question.text));
  }, [questions]);

  useEffect(() => {
    setAreAnswersEntered(
      answers.every((answerBlock) =>
        answerBlock.every((answer) => answer.text),
      ),
    );
    setIsCheckboxChecked(
      answers.every((answerBlock) =>
        answerBlock.some((answer) => answer.isCorrect),
      ),
    );
  }, [answers]);

  useEffect(() => {
    setShowLoading(questions.length === 0);
  }, [questions]);

  const handleQuestionChange = useCallback(
    (i, value) => {
      setQuestions((prevQuestions) =>
        prevQuestions.map((question, index) =>
          index === i ? { ...question, text: value } : question,
        ),
      );
    },
    [setQuestions],
  );

  const handleAnswerChange = useCallback(
    (i, j, value, isCorrect) => {
      setAnswers((prevAnswers) =>
        prevAnswers.map((answerBlock, answerBlockIndex) =>
          answerBlockIndex === i
            ? answerBlock.map((answer, answerIndex) =>
                answerIndex === j
                  ? { ...answer, text: value, isCorrect }
                  : answer,
              )
            : answerBlock,
        ),
      );
    },
    [setAnswers],
  );

  const handleSave = (event) => {
    event.preventDefault();

    const successMessage ='Data saved successfully!';

      toast.success(successMessage, {
        position: 'bottom-center',
        autoClose: 1000,
      });
  };

  const handleRemoveQuestion = (index) => {
    const newQuestions = [...questions];
    newQuestions.splice(index, 1);
    setQuestions(newQuestions);

    const newForm = { ...form, numQuestions: form.numQuestions - 1 };
    updateForm(newForm);
    setForm(newForm);
  };
  const [showLoading, setShowLoading] = useState(false);

  const isDisabled = () =>
    !areQuestionsEntered ||
    !areAnswersEntered ||
    !isCheckboxChecked ||
    showLoading;

  return (
    <Styled.Form onSubmit={handleSave}>
      {questions.length === 0 ? (
        <Styled.ErrorText>Please fill out all test details</Styled.ErrorText>
      ) : (
        questions.map((question, qIndex) => (
          <>
            <Question
              key={`question-${qIndex}`}
              question={question}
              qIndex={qIndex}
              handleQuestionChange={handleQuestionChange}
              answers={answers}
              handleAnswerChange={handleAnswerChange}
              handleRemoveQuestion={handleRemoveQuestion} 
            />

            <Validation
              areQuestionsEntered={areQuestionsEntered}
              areAnswersEntered={areAnswersEntered}
              isCheckboxChecked={isCheckboxChecked}
            />

            <Styled.Line />
          </>
        ))
      )}
      {questions.length > 0 && (
        <button
          type="submit"
          className="creation-button"
          disabled={isDisabled()}
        >
          <FontAwesomeIcon icon={faSave} /> Save
        </button>
      )}
    </Styled.Form>
  );
};

QuestionForm.propTypes = {
  numQuestions: PropTypes.number.isRequired,
  numAnswers: PropTypes.number.isRequired,
  formProp: PropTypes.object,
  updateForm: PropTypes.func,
};

Question.propTypes = {
  question: PropTypes.shape({
    text: PropTypes.string,
  }).isRequired,
  qIndex: PropTypes.number.isRequired,
  handleQuestionChange: PropTypes.func.isRequired,
  answers: PropTypes.arrayOf(
    PropTypes.shape({
      text: PropTypes.string,
    }),
  ).isRequired,
  handleAnswerChange: PropTypes.func.isRequired,
  handleRemoveQuestion: PropTypes.func.isRequired,
};

export default QuestionForm;
