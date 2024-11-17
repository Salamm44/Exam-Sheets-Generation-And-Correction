import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import { Tab, Nav } from 'react-bootstrap';
import './MainPage.css';
import Tab1 from './tab1/Tab1';
import Tab2 from './Tab2';
import Tab3 from './Tab3';

const MainPage = () => {
    const [activeTab, setActiveTab] = useState('tab1');
    const [activePoint, setActivePoint] = useState('point1'); 
    

  return (
<Router>
  <Tab.Container defaultActiveKey="tab1">
    <Nav variant="tabs">
      <Nav.Item>
        <Nav.Link as="div" eventKey="tab1" onClick={() => setActiveTab('tab1')}>
          <Link to="/tab1">Generating Test</Link>
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as="div" eventKey="tab2" onClick={() => setActiveTab('tab2')}>
          <Link to="/tab2">Upload Answers</Link>
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link as="div" eventKey="tab3" onClick={() => setActiveTab('tab3')}>
          <Link to="/tab3">Show Results</Link>
        </Nav.Link>
      </Nav.Item>
    </Nav>
    <Tab.Content>
      {activeTab === 'tab1' && <Tab1 activePoint={activePoint} setActivePoint={setActivePoint} />} 
      {activeTab === 'tab2' && <Tab2 />}
      {activeTab === 'tab3' && <Tab3 />}
    </Tab.Content>
  </Tab.Container>
</Router>
  );
};

export default MainPage;