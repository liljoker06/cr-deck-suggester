import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useCard } from '../hooks/useApi';

export default function CardDetail() {
  const { cardNumber } = useParams();
  const navigate = useNavigate();
  const { card, loading, error } = useCard(cardNumber);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement de la carte...</p>
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
          <button 
            onClick={() => navigate('/cartes')}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Retour aux cartes
          </button>
        </div>
      </div>
    );
  }

  if (!card) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-yellow-400 text-6xl mb-4">🃏</div>
          <h2 className="text-white text-2xl mb-2">Carte non trouvée</h2>
          <p className="text-gray-300">La carte "{cardNumber}" n'existe pas</p>
          <button 
            onClick={() => navigate('/cartes')}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Retour aux cartes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      {/* Bouton retour */}
      <div className="pt-20 pb-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <button 
            onClick={() => navigate('/cartes')}
            className="flex items-center text-yellow-400 hover:text-yellow-300 transition-colors mb-6"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Retour aux cartes
          </button>
        </div>
      </div>

      {/* Détails de la carte */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="bg-white/10 backdrop-blur-sm rounded-xl border border-white/20 overflow-hidden">
          <div className="p-8">
            {/* En-tête avec image et infos principales */}
            <div className="flex flex-col md:flex-row gap-8 mb-8">
              {/* Image de la carte */}
              <div className="flex-shrink-0">
                <div className="w-48 h-64 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-lg shadow-2xl flex items-center justify-center">
                  {card.image ? (
                    <img 
                      src={card.image} 
                      alt={card.name}
                      className="w-full h-full object-cover rounded-lg"
                    />
                  ) : (
                    <div className="text-white text-6xl">
                      {card.category === 'Troops' ? '👥' : 
                       card.category === 'Spells' ? '⚡' : 
                       card.category === 'Buildings' ? '🏰' : '🃏'}
                    </div>
                  )}
                </div>
              </div>

              {/* Informations principales */}
              <div className="flex-1">
                <h1 className="text-4xl font-bold text-white mb-4">{card.name}</h1>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
                  <div className="bg-white/5 rounded-lg p-4">
                    <h3 className="text-yellow-400 text-sm font-semibold mb-2 flex items-center gap-2">
                      <img src="/elixir.png" alt="Élixir" className="w-4 h-4" />
                      Coût d'Élixir
                    </h3>
                    <p className="text-white text-2xl font-bold">{card.elixir_cost}</p>
                  </div>
                  
                  <div className="bg-white/5 rounded-lg p-4">
                    <h3 className="text-yellow-400 text-sm font-semibold mb-2">📂 Catégorie</h3>
                    <p className="text-white text-lg">{card.category}</p>
                  </div>

                  {card.count && (
                    <div className="bg-white/5 rounded-lg p-4">
                      <h3 className="text-yellow-400 text-sm font-semibold mb-2">👥 Nombre</h3>
                      <p className="text-white text-lg">{card.count}</p>
                    </div>
                  )}

                  {card.evolution && (
                    <div className="bg-white/5 rounded-lg p-4">
                      <h3 className="text-yellow-400 text-sm font-semibold mb-2">🧬 Évolution</h3>
                      <p className="text-green-400 text-lg">✓ Disponible</p>
                    </div>
                  )}
                </div>

                {/* Description */}
                {card.description && (
                  <div className="bg-white/5 rounded-lg p-4">
                    <h3 className="text-yellow-400 text-sm font-semibold mb-2">📋 Description</h3>
                    <p className="text-gray-300 leading-relaxed">{card.description}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Statistiques détaillées */}
            <div className="border-t border-white/20 pt-8">
              <h2 className="text-2xl font-bold text-white mb-6">📊 Statistiques</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {card.hitpoints && (
                  <div className="bg-red-500/20 rounded-lg p-4 border border-red-500/30">
                    <h3 className="text-red-400 text-sm font-semibold mb-2">❤️ Points de Vie</h3>
                    <p className="text-white text-xl font-bold">{card.hitpoints}</p>
                  </div>
                )}
                
                {card.damage && (
                  <div className="bg-orange-500/20 rounded-lg p-4 border border-orange-500/30">
                    <h3 className="text-orange-400 text-sm font-semibold mb-2">⚔️ Dégâts</h3>
                    <p className="text-white text-xl font-bold">{card.damage}</p>
                  </div>
                )}
                
                {card.dps && (
                  <div className="bg-yellow-500/20 rounded-lg p-4 border border-yellow-500/30">
                    <h3 className="text-yellow-400 text-sm font-semibold mb-2">💥 DPS</h3>
                    <p className="text-white text-xl font-bold">{card.dps}</p>
                  </div>
                )}
                
                {card.range && (
                  <div className="bg-green-500/20 rounded-lg p-4 border border-green-500/30">
                    <h3 className="text-green-400 text-sm font-semibold mb-2">🎯 Portée</h3>
                    <p className="text-white text-xl font-bold">{card.range}</p>
                  </div>
                )}

                {card.hit_speed && (
                  <div className="bg-blue-500/20 rounded-lg p-4 border border-blue-500/30">
                    <h3 className="text-blue-400 text-sm font-semibold mb-2">⏱️ Vitesse d'Attaque</h3>
                    <p className="text-white text-xl font-bold">{card.hit_speed}s</p>
                  </div>
                )}

                {card.special_damage && card.special_damage !== "N/A" && (
                  <div className="bg-purple-500/20 rounded-lg p-4 border border-purple-500/30">
                    <h3 className="text-purple-400 text-sm font-semibold mb-2">🔥 Dégâts Spéciaux</h3>
                    <p className="text-white text-xl font-bold">{card.special_damage}</p>
                  </div>
                )}
              </div>
            </div>

            {/* Informations d'évolution */}
            {card.evolution && (
              <div className="border-t border-white/20 pt-8 mt-8">
                <h2 className="text-2xl font-bold text-white mb-6">🧬 Évolution</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  {/* Image d'évolution */}
                  {card.evolution_image && (
                    <div className="bg-white/5 rounded-lg p-4">
                      <h3 className="text-yellow-400 text-sm font-semibold mb-3">🖼️ Image d'Évolution</h3>
                      <img 
                        src={card.evolution_image} 
                        alt={`${card.name} évoluée`}
                        className="w-full h-32 object-contain rounded-lg bg-white/10"
                      />
                    </div>
                  )}

                  {/* Statistiques d'évolution */}
                  <div className="bg-white/5 rounded-lg p-4">
                    <h3 className="text-yellow-400 text-sm font-semibold mb-3">📈 Statistiques d'Évolution</h3>
                    <div className="space-y-2">
                      {card.evolution.cycles && (
                        <div className="flex justify-between">
                          <span className="text-gray-300">Cycles:</span>
                          <span className="text-white font-bold">{card.evolution.cycles}</span>
                        </div>
                      )}
                      {card.evolution.overall_cost && (
                        <div className="flex justify-between">
                          <span className="text-gray-300">Coût total:</span>
                          <span className="text-white font-bold">{card.evolution.overall_cost}</span>
                        </div>
                      )}
                      {card.evolution.stat_boost && (
                        <div className="flex justify-between">
                          <span className="text-gray-300">Amélioration:</span>
                          <span className="text-green-400 font-bold">{card.evolution.stat_boost}</span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
