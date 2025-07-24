import React, { useState } from 'react'
import { useDecks } from '../hooks/useApi'
import Deck from '../components/card/Deck'

export default function Decks() {
  const [filters, setFilters] = useState({
    arena_number: '',
    limit: 20
  });
  
  const { decks, loading, error } = useDecks(filters);

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  const resetFilters = () => {
    setFilters({
      arena_number: '',
      limit: 20
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement des decks...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <h2 className="text-white text-2xl mb-2">Erreur de chargement</h2>
          <p className="text-gray-300">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      {/* Header */}
      <div className="pt-20 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white sm:text-5xl">
              🎴 <span className="text-yellow-400">Decks</span> Clash Royale
            </h1>
            <p className="mt-4 text-xl text-gray-300">
              Découvrez les meilleurs decks pour dominer le jeu
            </p>
          </div>
        </div>
      </div>

      {/* Filtres */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Arène
              </label>
              <select
                value={filters.arena_number}
                onChange={(e) => handleFilterChange('arena_number', e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <option value="">Toutes les arènes</option>
                {Array.from({length: 23}, (_, i) => i + 1).map(num => (
                  <option key={num} value={num}>Arène {num}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Nombre de decks
              </label>
              <select
                value={filters.limit}
                onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <option value={10}>10 decks</option>
                <option value={20}>20 decks</option>
                <option value={50}>50 decks</option>
                <option value={100}>100 decks</option>
              </select>
            </div>
            
            <div>
              <button
                onClick={resetFilters}
                className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors duration-200"
              >
                Réinitialiser
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Statistiques */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div className="text-center">
          <p className="text-gray-300">
            <span className="text-yellow-400 font-bold text-2xl">{decks.length}</span> decks trouvés
          </p>
        </div>
      </div>

      {/* Liste des decks */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {decks.map((deck, index) => (
            <div
              key={deck._id || index}
              className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6 hover:bg-white/20 transition-all duration-200"
            >
              {/* En-tête du deck */}
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-white font-bold text-lg">
                    {deck.name || `Deck ${index + 1}`}
                  </h3>
                  {deck.arena_number && (
                    <p className="text-gray-400 text-sm">Arène {deck.arena_number}</p>
                  )}
                </div>
                
                {deck.average_elixir_cost && (
                  <div className="bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                    ⚡ {deck.average_elixir_cost.toFixed(1)}
                  </div>
                )}
              </div>

              {/* Cartes du deck */}
              <div className="grid grid-cols-4 gap-2 mb-4">
                {deck.cards && deck.cards.length > 0 ? (
                  deck.cards.map((card, cardIndex) => (
                    <div
                      key={cardIndex}
                      className="aspect-square bg-gray-800 rounded-lg p-2 flex flex-col items-center justify-center text-center border border-gray-600"
                    >
                      {card.icon_url ? (
                        <img
                          src={card.icon_url}
                          alt={card.name}
                          className="w-8 h-8 object-contain mb-1"
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'block';
                          }}
                        />
                      ) : null}
                      <div 
                        className="text-lg" 
                        style={{ display: card.icon_url ? 'none' : 'block' }}
                      >
                        🃏
                      </div>
                      <span className="text-xs text-gray-300 truncate w-full" title={card.name}>
                        {card.name}
                      </span>
                      {card.elixir_cost && (
                        <span className="text-xs text-purple-300">
                          {card.elixir_cost}⚡
                        </span>
                      )}
                    </div>
                  ))
                ) : (
                  Array.from({length: 8}, (_, i) => (
                    <div
                      key={i}
                      className="aspect-square bg-gray-800 rounded-lg flex items-center justify-center text-gray-600 border border-gray-600"
                    >
                      <span className="text-lg">❓</span>
                    </div>
                  ))
                )}
              </div>

              {/* Statistiques du deck */}
              <div className="space-y-2">
                {deck.win_rate && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Taux de victoire:</span>
                    <span className="text-green-400 font-bold">
                      {(deck.win_rate * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
                
                {deck.usage_rate && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Taux d'utilisation:</span>
                    <span className="text-blue-400 font-bold">
                      {(deck.usage_rate * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
                
                {deck.battle_count && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400 text-sm">Batailles:</span>
                    <span className="text-yellow-400 font-bold">
                      {deck.battle_count.toLocaleString()}
                    </span>
                  </div>
                )}
              </div>

              {/* Tags/Catégories */}
              {deck.tags && deck.tags.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-1">
                  {deck.tags.slice(0, 3).map((tag, tagIndex) => (
                    <span
                      key={tagIndex}
                      className="bg-blue-600 text-white px-2 py-1 rounded text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {decks.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🎴</div>
            <h3 className="text-white text-xl mb-2">Aucun deck trouvé</h3>
            <p className="text-gray-400">Essayez de modifier vos filtres ou vérifiez que les données sont disponibles</p>
          </div>
        )}
      </div>
    </div>
  );
}
