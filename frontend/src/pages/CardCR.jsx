import React, { useState } from 'react'
import { useCards } from '../hooks/useApi'

export default function CardCR() {
  const [filters, setFilters] = useState({
    category: '',
    rarity: '',
    limit: 50
  });
  
  const { cards, loading, error } = useCards(filters);

  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  const resetFilters = () => {
    setFilters({
      category: '',
      rarity: '',
      limit: 50
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement des cartes...</p>
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
              🃏 <span className="text-yellow-400">Cartes</span> Clash Royale
            </h1>
            <p className="mt-4 text-xl text-gray-300">
              Découvrez toutes les cartes disponibles dans Clash Royale
            </p>
          </div>
        </div>
      </div>

      {/* Filtres */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Catégorie
              </label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <option value="">Toutes les catégories</option>
                <option value="Troop">Troupes</option>
                <option value="Spell">Sorts</option>
                <option value="Building">Bâtiments</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Rareté
              </label>
              <select
                value={filters.rarity}
                onChange={(e) => handleFilterChange('rarity', e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <option value="">Toutes les raretés</option>
                <option value="Common">Commune</option>
                <option value="Rare">Rare</option>
                <option value="Epic">Épique</option>
                <option value="Legendary">Légendaire</option>
                <option value="Champion">Champion</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Limite
              </label>
              <select
                value={filters.limit}
                onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
              >
                <option value={25}>25 cartes</option>
                <option value={50}>50 cartes</option>
                <option value={100}>100 cartes</option>
                <option value={200}>Toutes</option>
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
            <span className="text-yellow-400 font-bold text-2xl">{cards.length}</span> cartes trouvées
          </p>
        </div>
      </div>

      {/* Grille des cartes */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          {cards.map((card, index) => (
            <div
              key={card.name || index}
              className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-4 hover:bg-white/20 transition-all duration-200 transform hover:scale-105"
            >
              {/* Image de la carte */}
              <div className="aspect-square rounded-lg mb-3 flex items-center justify-center">
                {card.className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800" ? (
                  <img
                    src={card.image}
                    alt={card.name}
                    className="w-64 h-64 object-contain"
                    referrerPolicy="no-referrer"
                    onError={() => console.log("Image échouée")}
                  />
                ) : null}
                <div className="text-4xl" style={{ display: card.className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800" ? 'none' : 'block' }}>
                  {card.category === 'Troop' ? '👥' : 
                   card.category === 'Spell' ? '⚡' : 
                   card.category === 'Building' ? '🏰' : '🃏'}
                </div>
              </div>
              
              {/* Informations de la carte */}
              <div className="text-center">
                <h3 className="text-white font-bold text-sm mb-1 truncate" title={card.name}>
                  {card.name}
                </h3>
                
                <div className="flex justify-between items-center text-xs mb-2">
                 
                  {card.elixir_cost && (
                    <span className="bg-purple-600 text-white px-2 py-1 rounded text-xs font-medium">
                      {card.elixir_cost} ⚡
                    </span>
                  )}
                </div>
                
                <div className="text-gray-400 text-xs">
                  {card.category || 'Catégorie inconnue'}
                </div>
                
                {card.evolution_ids && card.evolution_ids.length > 0 && (
                  <div className="mt-2">
                    <span className="bg-green-600 text-white px-2 py-1 rounded text-xs font-medium">
                      🔄 Évolution
                    </span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {cards.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-white text-xl mb-2">Aucune carte trouvée</h3>
            <p className="text-gray-400">Essayez de modifier vos filtres</p>
          </div>
        )}
      </div>
    </div>
  );
}
