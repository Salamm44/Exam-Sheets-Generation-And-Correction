import styled from 'styled-components';

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 0px 15px 0px rgba(0, 0, 0, 0.2);
  width: 50%;
  min-height: 450px;
  height: auto;
  margin: auto;
`;

export const Input = styled.input`
  display: flex;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  width: 100%;
  box-sizing: border-box;
`;

export const QuestionBlock = styled.div`
  width: 70%;
`;

export const H3 = styled.h3`
  margin: 0px;
`;

export const Line = styled.hr`
  color: #ccc;
  height: 2px;
  width: 70%;
  margin: 16px 0;
  border: none;
  background-color: #ccc;
`;


export const ErrorText = styled.p`
  color: red;
  font-size: 18px;
`;

export const RemoveButton = styled.button`
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: #8C0303;
  color: white;
  font-size: 14px;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  margin: 0 10px;
`;

export const QuestionRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;