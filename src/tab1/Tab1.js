import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faChevronLeft,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import TestDetails from './TestDetails/TestDetails';
import TestQuestions from './TestQuestions/TestQuestions';
import PreviewPDF from './PreviewPDF/PreviewPDF';

const tabs = ['Test Details', 'Test Questions', 'Preview & Download PDF'];
const components = {
  'Test Details': <TestDetails />,
  'Test Questions': <TestQuestions />,
  'Preview & Download PDF': <PreviewPDF />
};

const Tab1 = () => {
  const [activePoint, setActivePoint] = useState(tabs[0]);
  const [visitedPoints, setVisitedPoints] = useState([]);

  return (
    <>
      <div className="progress-container">
        <div className="progress-line">
          {tabs.map((point, index) => (
            <div
              key={index}
              className={`progress-step ${
                activePoint === point ? 'active' : ''
              }`}
              onClick={() => {
                if (!visitedPoints.includes(activePoint)) {
                  setVisitedPoints((prevVisitedPoints) => [
                    ...prevVisitedPoints,
                    activePoint,
                  ]);
                }
                setActivePoint(point);
              }}
            >
              {(activePoint === point || visitedPoints.includes(point)) && (
                <div key={index + 'a'}>{index + 1}</div>
              )}
            </div>
          ))}
        </div>
      </div>
      {components[activePoint]}
    </>
  );
};

export default Tab1;
