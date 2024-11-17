import React, { useState } from 'react';
import styled from 'styled-components';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye } from '@fortawesome/free-solid-svg-icons';
import { jsPDF } from 'jspdf';
import { GlobalWorkerOptions } from 'pdfjs-dist';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';
import useLocalStorage from '../hooks/useLocalStorage';

GlobalWorkerOptions.workerSrc = pdfjsWorker;

const StyledDiv = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  font-family: 'Helvetica Neue', Arial, sans-serif;
  width: 100%;
`;

const StyledButton = styled.button`
  background-color: #8C0303;
  border: none;
  color: white;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  display: inline-block; 

  &:disabled {
    background-color: gray;
    cursor: not-allowed;
  }
`;

const StyledBlock = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
  width: 80%;
  height: 480px;
  margin: 20px 0;
  max-width: 800px;
`;

const ErrorText = styled.p`
  color: red;
  font-size: 18px;
`;

const IframeContainer = styled.div`
  width: 100%;
  height: 600px;
  overflow: hidden;
  position: relative;
`;

const Iframe = styled.iframe`
  width: 100%;
  height: 100%;
  border: none;
`;

const NavigationContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
`;

const PreviewPDF = () => {
  const [pdfBlob, setPdfBlob] = useState(null);
  const [questions, setQuestions] = useLocalStorage('questions', []);
  const [answers, serAnswers] = useLocalStorage('answers', []);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const isPreviewDisabled = () =>  questions.length === 0 || answers.length === 0;

  const addTemplateDetails = (doc, y) => {
    const testDetails = JSON.parse(localStorage.getItem('form'));
    console.log(testDetails);

    doc.setTextColor(169, 169, 169); 
    doc.setFontSize(12);

    const keys = Object.keys(testDetails).filter(key => key !== 'numAnswers' && key !== 'numQuestions' && key !== 'studentName' && key !== 'studentId');
    keys.forEach((key) => {
      doc.text(`${key}: ${testDetails[key]}`, 5, y);
      console.log(`Left side: ${key}: ${testDetails[key]} at (5, ${y})`);
      y += 5;
    });

    
    const  rightSideY = 14; 
    const studentIdX = 120;
  

 
    doc.text(`studentId: ${testDetails.studentId || ''}`, studentIdX, rightSideY); 
    console.log(`Right side: studentId: ${testDetails.studentId || 'empty'} at (${studentIdX}, ${rightSideY})`);

    doc.setTextColor(0, 0, 0); 
    doc.setFontSize(12);

    return y + 10; 
  };

  const generatePDF = async () => {
    const doc = new jsPDF();
    let y = 10; 

    y = addTemplateDetails(doc, y);

    let questionCount = 0;

    questions.forEach((question, index) => {
      const questionText = question.text ? question.text : question;
      if (typeof questionText !== 'string') {
        console.error('Question is not a string:', question);
        return;
      }

      if (questionCount === 7) {
        doc.addPage();
        y = 10;
        y = addTemplateDetails(doc, y);
        questionCount = 0;
      }

      const textX = 10;
      doc.text(questionText, textX, y);
      y += 10; 
      questionCount++;

      answers[index].forEach((answer) => {
        if (typeof answer === 'object' && answer.text) {
          doc.rect(15, y - 3, 3, 3); 
          doc.text(answer.text, 20, y); 
          y += 5; 
        } else {
          console.error('Answer is not a string:', answer);
        }
      });
      y += 10;
    });

    const pdfBlob = doc.output('blob');
    setPdfBlob(URL.createObjectURL(pdfBlob));
    setTotalPages(doc.internal.getNumberOfPages());
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <StyledDiv>
      <StyledBlock>
        {pdfBlob ? (
          // display pdf
          <IframeContainer>
            <Iframe src={`${pdfBlob}#page=${currentPage}`} type="application/pdf" title="PDF Preview" />
            <NavigationContainer>
              <button onClick={handlePreviousPage} disabled={currentPage === 1}>Previous</button>
              <span>Page {currentPage} of {totalPages}</span>
              <button onClick={handleNextPage} disabled={currentPage === totalPages}>Next</button>
            </NavigationContainer>
          </IframeContainer>
        ) : (
          <>
            {isPreviewDisabled() && <ErrorText>Please fill out all questions and answers.</ErrorText>}
            <StyledButton onClick={generatePDF} disabled={isPreviewDisabled()}>
              <span style={{ marginRight: '8px' }}>
                <FontAwesomeIcon icon={faEye} />
              </span>
              Preview PDF
            </StyledButton>
          </>
        )}
      </StyledBlock>
    </StyledDiv>
  );
};

export default PreviewPDF;
