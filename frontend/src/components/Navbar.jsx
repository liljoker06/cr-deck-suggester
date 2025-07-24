import React, { useState } from 'react'
import { useGlobalStats, useArenas } from '../hooks/useApi';

export default function Navbar() {
  const { stats, loading, error } = useGlobalStats();
  const { arenas, loading: arenasLoading, error: arenasError } = useArenas();
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')

  const arenes = arenas.map(arena => ({
    name: `${arena.name} (Arena ${arena.number})`,
    path: `/arena/${arena.number}`,
    number: arena.number,
    minTrophies: arena.min_trophies
  })).sort((a, b) => a.number - b.number)

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      console.log('Searching for:', searchQuery)
    }
  }

  return (
    <nav className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800 shadow-xl fixed w-full top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">

          {/* Logo */}
          <div className="flex-shrink-0 flex items-center">
            <a href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <img src="/CR-Logo.png" alt="Clash Royale Logo" className="h-10 w-auto" />
              <span className="text-xl font-bold text-yellow-400 hidden sm:block">Mousieur DeckSVP</span>
            </a>
          </div>

          {/* Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {/* Arènes */}
            <div className="relative group">
              <button className="text-white hover:text-yellow-400 px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center">
                Arènes
                <svg className="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              <div className="absolute left-0 mt-2 w-56 bg-gray-800 rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                <div className="py-2 max-h-80 overflow-y-auto">
                  {arenes.map((arena, index) => (
                    <a
                      key={index}
                      href={arena.path}
                      className="block px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-yellow-400 transition-colors"
                    >
                      {arena.name}
                    </a>
                  ))}
                </div>
              </div>
            </div>

            {/* Autre lien */}
            <a href="/arena" className="text-white hover:text-yellow-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Arènes
            </a>
            <a href="/cartes" className="text-white hover:text-yellow-400 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Cartes
            </a>
          </div>

          {/* Box de recherche */}
          <div className="hidden md:block">
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                placeholder="Chercher des cartes, decks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-gray-800 text-white placeholder-gray-400 px-4 py-2 pr-10 rounded-lg border border-gray-600 focus:border-yellow-400 focus:ring-1 focus:ring-yellow-400 focus:outline-none transition-colors w-64"
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-yellow-400 transition-colors"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>
          </div>

          {/* Pour mobile : bouton */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-yellow-400 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-yellow-400"
            >
              <span className="sr-only">Open main menu</span>
              {!isMenuOpen ? (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              ) : (
                <svg className="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Menu mobile */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-gray-900 border-t border-gray-700">
            {/* Recherche */}
            <form onSubmit={handleSearch} className="relative mb-4">
              <input
                type="text"
                placeholder="Chercher des cartes, des decks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-800 text-white placeholder-gray-400 px-4 py-2 pr-10 rounded-lg border border-gray-600 focus:border-yellow-400 focus:ring-1 focus:ring-yellow-400 focus:outline-none"
              />
              <button
                type="submit"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-yellow-400"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </form>

            {/* Liens */}
            <a href="/decks" className="text-gray-300 hover:text-yellow-400 block px-3 py-2 rounded-md text-base font-medium">
              Decks
            </a>
            <a href="/cartes" className="text-gray-300 hover:text-yellow-400 block px-3 py-2 rounded-md text-base font-medium">
              Cartes
            </a>
            <a href="/leaderboard" className="text-gray-300 hover:text-yellow-400 block px-3 py-2 rounded-md text-base font-medium">
              Leaderboard
            </a>
            
            {/* Arènes */}
            <div className="pt-2">
              <p className="text-yellow-400 px-3 py-2 text-sm font-semibold">Arènes</p>
              <div className="max-h-40 overflow-y-auto">
                {arenes.slice(0, 8).map((arena, index) => (
                  <a
                    key={index}
                    href={arena.path}
                    className="text-gray-300 hover:text-yellow-400 block px-6 py-1 text-sm"
                  >
                    {arena.name}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}
