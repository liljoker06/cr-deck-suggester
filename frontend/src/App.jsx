import React from 'react'
import {Route, Routes} from 'react-router-dom';

/// import pages
import Home from './pages/Home.jsx';
import CardCR from './pages/CardCR.jsx';

import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';


export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/card" element={<CardCR />} />
      </Routes>
      <Footer />
    </>
  )
}

