import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useArenas } from '../hooks/useApi'

export default function Arenas() {
  const navigate = useNavigate();
  const { arenas, loading, error } = useArenas();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement des arènes...</p>
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

  // Trier les arènes par nombre de trophées minimum
  const sortedArenas = [...arenas].sort((a, b) => a.min_trophies - b.min_trophies);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      {/* Header */}
      <div className="pt-20 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white sm:text-5xl">
              🏛️ <span className="text-yellow-400">Arènes</span> Clash Royale
            </h1>
            <p className="mt-4 text-xl text-gray-300">
              Progressez à travers toutes les arènes de Clash Royale
            </p>
          </div>
        </div>
      </div>

      {/* Statistiques */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
            <div className="text-3xl font-bold text-yellow-400">{arenas.length}</div>
            <div className="text-gray-300 mt-1">Arènes disponibles</div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
            <div className="text-3xl font-bold text-yellow-400">
              {sortedArenas.length > 0 ? sortedArenas[0].min_trophies : 0}
            </div>
            <div className="text-gray-300 mt-1">Trophées minimum</div>
          </div>
          
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
            <div className="text-3xl font-bold text-yellow-400">
              {sortedArenas.length > 0 ? sortedArenas[sortedArenas.length - 1].min_trophies : 0}+
            </div>
            <div className="text-gray-300 mt-1">Trophées maximum</div>
          </div>
        </div>
      </div>

      {/* Liste des arènes */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sortedArenas.map((arena, index) => (
            <div
              key={arena.number || index}
              className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6 hover:bg-white/20 transition-all duration-200 transform hover:scale-105 cursor-pointer"
              onClick={() => navigate(`/arena/${arena.number}`)}
            >
              {/* En-tête de l'arène */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {arena.number}
                  </div>
                  <div>
                    <h3 className="text-white font-bold text-lg truncate" title={arena.name}>
                      {arena.name}
                    </h3>
                    <p className="text-gray-400 text-sm">Arène {arena.number}</p>
                  </div>
                </div>
              </div>

              {/* Image de l'arène */}
              <div className="aspect-video bg-gray-800 rounded-lg mb-4 flex items-center justify-center">
                {arena.image_url ? (
                  <img
                    src={arena.image_url}
                    alt={arena.name}
                    className="w-full h-full object-cover rounded-lg"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div 
                  className="text-6xl text-gray-600" 
                  style={{ display: arena.image_url ? 'none' : 'flex' }}
                >
                  🏛️
                </div>
              </div>

              {/* Informations de l'arène */}
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Trophées requis:</span>
                  <span className="text-yellow-400 font-bold">
                    {arena.min_trophies.toLocaleString()} 🏆
                  </span>
                </div>

                {arena.chest_reward_multiplier && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Multiplicateur coffres:</span>
                    <span className="text-green-400 font-bold">
                      x{arena.chest_reward_multiplier}
                    </span>
                  </div>
                )}

                {arena.shop_chest_reward_multiplier && (
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Boutique:</span>
                    <span className="text-blue-400 font-bold">
                      x{arena.shop_chest_reward_multiplier}
                    </span>
                  </div>
                )}
              </div>

              {/* Badge de difficulté */}
              <div className="mt-4 flex items-center justify-between">
                <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                  arena.min_trophies < 1000 ? 'bg-green-600 text-white' :
                  arena.min_trophies < 3000 ? 'bg-yellow-600 text-black' :
                  arena.min_trophies < 5000 ? 'bg-orange-600 text-white' :
                  'bg-red-600 text-white'
                }`}>
                  {arena.min_trophies < 1000 ? '🟢 Débutant' :
                   arena.min_trophies < 3000 ? '🟡 Intermédiaire' :
                   arena.min_trophies < 5000 ? '🟠 Avancé' :
                   '🔴 Expert'}
                </span>
                
                {/* Bouton pour voir les détails */}
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/arena/${arena.number}`);
                  }}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs font-medium transition-colors flex items-center space-x-1"
                >
                  <span>Détails</span>
                  <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>

        {arenas.length === 0 && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🏛️</div>
            <h3 className="text-white text-xl mb-2">Aucune arène trouvée</h3>
            <p className="text-gray-400">Les données des arènes ne sont pas encore disponibles</p>
          </div>
        )}
      </div>
    </div>
  );
}
