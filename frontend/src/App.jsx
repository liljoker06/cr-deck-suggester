import React from 'react'
import {Route, Routes} from 'react-router-dom';

/// import pages
import Home from './pages/Home.jsx';
import CardCR from './pages/CardCR.jsx';


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/card" element={<CardCR />} />
    </Routes>
  )
}

