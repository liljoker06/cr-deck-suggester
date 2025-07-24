import React from 'react'
import {Route, Routes} from 'react-router-dom';

/// import pages
import Home from './pages/Home.jsx';
import CardCR from './pages/CardCR.jsx';
import Arenas from './pages/Arenas.jsx';
import ArenaDetail from './pages/ArenaDetail.jsx';
import Decks from './pages/Decks.jsx';
import DeckBuilder from './pages/DeckBuilder.jsx';

import Navbar from './components/Navbar.jsx';
import Footer from './components/Footer.jsx';


export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cards" element={<CardCR />} />
        <Route path="/cartes" element={<CardCR />} />
        <Route path="/arenas" element={<Arenas />} />
        <Route path="/arena/:arenaNumber" element={<ArenaDetail />} />
        <Route path="/decks" element={<Decks />} />
        <Route path="/creer-deck" element={<DeckBuilder />} />
      </Routes>
      <Footer />
    </>
  )
}

