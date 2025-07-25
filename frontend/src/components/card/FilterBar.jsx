import React from 'react';

export default function FilterBar({ filters, onFilterChange, onResetFilters, cardsCount }) {
  const handleFilterChange = (filterName, value) => {
    onFilterChange(filterName, value);
  };

  const resetFilters = () => {
    onResetFilters();
  };

  const categories = [
    { value: '', label: 'Toutes les catégories' },
    { value: 'Troops', label: '👥 Troupes' },
    { value: 'Spells', label: '⚡ Sorts' },
    { value: 'Buildings', label: '🏰 Bâtiments' }
  ];

  const elixirCosts = [
    { value: '', label: 'Tous les coûts' },
    { value: '1', label: '1 ⚡' },
    { value: '2', label: '2 ⚡' },
    { value: '3', label: '3 ⚡' },
    { value: '4', label: '4 ⚡' },
    { value: '5', label: '5 ⚡' },
    { value: '6', label: '6 ⚡' },
    { value: '7', label: '7 ⚡' },
    { value: '8', label: '8 ⚡' },
    { value: '9', label: '9 ⚡' },
    { value: '10', label: '10 ⚡' }
  ];

  const hasEvolutionOptions = [
    { value: '', label: 'Toutes' },
    { value: 'true', label: '🔄 Avec évolution' },
    { value: 'false', label: '❌ Sans évolution' }
  ];

  const limitOptions = [
    { value: 25, label: '25 cartes' },
    { value: 50, label: '50 cartes' },
    { value: 100, label: '100 cartes' },
    { value: 200, label: 'Toutes les cartes' }
  ];

  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white">🔍 Filtres de recherche</h2>
        <div className="flex items-center gap-4">
          <div className="text-gray-300 text-sm">
            <span className="text-yellow-400 font-bold">{cardsCount}</span> carte(s) trouvée(s)
          </div>
          {Object.values(filters).some(value => value && value !== 50) && (
            <div className="text-xs text-blue-400 bg-blue-900/50 px-2 py-1 rounded">
              Filtres actifs
            </div>
          )}
        </div>
      </div>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        {/* Catégorie */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Catégorie
          </label>
          <select
            value={filters.category || ''}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400 text-sm"
          >
            {categories.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Coût en élixir */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Coût élixir
          </label>
          <select
            value={filters.elixir_cost || ''}
            onChange={(e) => handleFilterChange('elixir_cost', e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400 text-sm"
          >
            {elixirCosts.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Évolution */}
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Évolution
          </label>
          <select
            value={filters.has_evolution || ''}
            onChange={(e) => handleFilterChange('has_evolution', e.target.value)}
            className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400 text-sm"
          >
            {hasEvolutionOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* Bouton de réinitialisation */}
        <div className="flex items-end">
          <button
            onClick={resetFilters}
            className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors duration-200 text-sm font-medium"
            title="Réinitialiser tous les filtres"
          >
            Reset
          </button>
        </div>
      </div>

      {/* Limite d'affichage en bas */}
      <div className="mt-4 pt-4 border-t border-gray-600">
        <div className="flex items-center justify-between">
          <label className="block text-sm font-medium text-gray-300">
            Nombre de cartes à afficher
          </label>
          <select
            value={filters.limit || 50}
            onChange={(e) => handleFilterChange('limit', parseInt(e.target.value))}
            className="px-3 py-2 bg-gray-800 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-yellow-400 text-sm"
          >
            {limitOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}
